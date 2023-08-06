import importlib
import os
import pkgutil
import xml.etree.ElementTree as XmlTree
from typing import Optional

from blockly_executor import Action
from blockly_executor import ExtException
from blockly_executor import Helper
from blockly_executor.core.exceptions import DeferredOperation, StepForward, LimitCommand
from blockly_executor.core.blocks.procedures_defnoreturn import ProceduresDefnoreturn
from blockly_executor.core.blocks.procedures_defreturn import ProceduresDefreturn
from blockly_executor.core.blocks.root import Root


class BlocklyExecutor:
    ns = {'b': 'https://developers.google.com/blockly/xml'}
    _blocks_index = None
    _blocks_class = {}

    def __init__(self, *, step=None, step_workspace=None, logger=None, plugin=None, step_by_step=None,
                 debug=None, selected=None, **kwargs):
        self.functions = None
        self.variables = None
        self.robot = None
        self.root = None
        self.multi_thread_mode = False
        self.step = step
        self.step_workspace = step_workspace
        _selected = selected
        self.selected = None if self.step == _selected else _selected
        self.logger = logger
        self.step_by_step = bool(kwargs.get('step_by_step', debug))
        self.next_step = True if self.step_by_step and not self.step else None
        self.extend_plugin = plugin
        self.commands = []
        self.gather = []
        self.commands_result = {}
        self.workspace_name = None
        self.action: Optional[Action] = None

    @property
    def blocks_index(self) -> dict:
        if self._blocks_index is not None:
            return self._blocks_index

        import blockly_executor.plugins
        plugins = {
            name: importlib.import_module(name)
            for finder, name, ispkg
            in pkgutil.iter_modules(blockly_executor.plugins.__path__, blockly_executor.plugins.__name__ + ".")
        }
        plugins['blockly_executor.core'] = blockly_executor.core
        if self.extend_plugin:
            plugins[self.extend_plugin] = importlib.import_module(self.extend_plugin)

        self._blocks_index = {}
        for plugin_name in plugins:
            plugin = plugins[plugin_name]
            blocks_dir = os.path.join(plugin.__path__[0], 'blocks')
            if not os.path.isdir(blocks_dir):
                continue
            blocks_files = os.listdir(blocks_dir)
            for file_name in blocks_files:
                if file_name[-3:] != '.py' or file_name == '__init__.py':
                    continue
                self._blocks_index[file_name[:-3]] = plugin_name
                pass
        return self._blocks_index

    def get_block_class(self, block_name):
        block_name = block_name.lower()
        try:
            return self._blocks_class[block_name]
        except KeyError:
            pass
        try:
            index = self.blocks_index[block_name]
        except [KeyError, TypeError]:
            raise ExtException(message='Block handler not found', detail=block_name)

        try:
            full_name = f'{index}.blocks.{block_name}.{Helper.to_camel_case(block_name)}'
            self._blocks_class[block_name] = Helper.get_class(full_name)
            return self._blocks_class[block_name]
        except Exception as err:
            raise ExtException(message='Block handler not found', detail=block_name, parent=err)

    @staticmethod
    def workspace_to_tree(workspace_xml):
        XmlTree.register_namespace('', 'https://developers.google.com/blockly/xml')
        return XmlTree.fromstring(workspace_xml)

    def _init_start_block(self, workspace_xml, endpoint, context):
        # стартуем с функции
        self.root = self.workspace_to_tree(workspace_xml)
        self.read_procedures_and_functions()
        self.variables = self.read_variables()
        if endpoint:
            try:
                block = self.functions[endpoint]
            except KeyError:
                context.operation['status'] = 'error'
                context.operation['data'] = f'not found endpoint {endpoint}'
                return context
        else:
            try:
                block = self.functions['main']
            except KeyError:
                block = Root.init(self, '', self.root, logger=self.logger)
        return block

    async def execute_nested(self, workspace_xml, context, *, endpoint=None, commands_result=None, workspace_name=None):
        self.workspace_name = workspace_name
        self.commands_result = commands_result
        start_block = self._init_start_block(workspace_xml, endpoint, context)

        return await start_block.execute(start_block.node, '', context, context.debug)

    async def execute(self, workspace_xml, context, *, endpoint=None, commands_result=None, workspace_name=None):
        self.workspace_name = workspace_name
        self.action = Action('BlocklyExecutor.execute')
        if commands_result:
            for command in commands_result:
                if 'uuid' in command:
                    self.commands_result[command['uuid']] = command
                else:
                    if command['status'] == 'error':
                        context.operation['status'] = 'error'
                        context.operation['data'] = command['data']
                        return context

        start_block = self._init_start_block(workspace_xml, endpoint, context)

        context.operation['commands'] = []
        try:
            if context.deferred:
                await self._execute_deferred(start_block, context)
            context.check_command_limit()

            self.logger.debug('')
            self.logger.debug('--------execute----------------------------')
            self.logger.debug(
                f'deferred:{len(context.deferred)}, '
                f'commands:{len(context.operation["commands"])}, '
                f'result:{len(self.commands_result.keys())}')

            result = await start_block.execute(start_block.node, '', context, context.debug)
            context.operation['data'] = result
            self.logger.debug('Complete')
            context.operation['status'] = 'complete'
        except DeferredOperation:
            self.logger.debug('raise DeferredOperation')
            pass
        except LimitCommand:
            self.logger.debug('raise LimitCommand')
            pass
        except StepForward as step:
            context.operation['step'] = step.args[0]
            context.operation['data'] = step.args[2]
            context.operation['variables'] = step.args[1].variables
            context.operation['step_workspace'] = step.args[3]
            self.logger.debug('raise StepForward')
        except ExtException as err:
            context.operation['status'] = 'error'
            context.operation['data'] = err.to_dict()
        except Exception as err:
            context.operation['status'] = 'error'
            error = ExtException(parent=err, skip_traceback=-2)
            context.operation['data'] = error.to_dict()
        context.operation['commands'] = self.commands
        # context.deferred = self.gather

        self.logger.debug(
            f'commands {len(self.commands)} command'
            f'gather:{len(self.gather)}, '
            f'result:{len(self.commands_result)}')
        # self.logger.debug(f'------------------')
        self.action.set_end()
        return context

    async def _execute_deferred(self, robot, context):
        self.logger.debug('')
        self.logger.debug('--------execute deferred--------------')
        self.logger.debug(
            f'deferred:{len(context.deferred)}, '
            f'commands:{len(context.operation["commands"])}, '
            f'result:{len(self.commands_result)}')
        # if len(self.commands_result) < len(context.deferred):
        #     raise Exception('не все ответы получены')
        _deferred = context.deferred
        _commands = context.operation['commands']
        context.operation['commands'] = []
        # context.deferred = []
        _delete = []
        for i in range(len(_deferred)):
            _context = context.init_deferred(_deferred[i])
            try:
                await robot.execute(robot.node, '', _context, _context.debug)
                _delete.append(i)
            except DeferredOperation as operation:
                context.add_deferred(operation)
                _delete.append(i)
                continue
        _delete.reverse()
        for elem in _delete:
            context.deferred.pop(elem)

    def read_procedures_and_functions(self):
        self.functions = {}
        for node in self.root.findall("./b:block[@type='procedures_defreturn']", self.ns):
            name = node.find("./b:field[@name='NAME']", self.ns).text
            self.functions[name] = ProceduresDefreturn.init(self, name, node, logger=self.logger)

        for node in self.root.findall("./b:block[@type='procedures_defnoreturn']", self.ns):
            name = node.find("./b:field[@name='NAME']", self.ns).text
            self.functions[name] = ProceduresDefnoreturn.init(self, name, node, logger=self.logger)

    def read_variables(self):
        result = {}
        for node in self.root.findall("./b:variables/b:variable", self.ns):
            name = node.text
            result[name] = None
        return result

    def set_friendly_id(self, workspace_xml):
        XmlTree.register_namespace('', 'https://developers.google.com/blockly/xml')
        self.root = XmlTree.fromstring(workspace_xml)
        self.read_procedures_and_functions()
        self.variables = self.read_variables()
        index = {}
        for func_name in self.functions:
            func = self.functions[func_name]
            try:
                func.set_friendly_id(func.node, index, self)

            except Exception as err:
                self.logger.warning(f'{func_name}: {err}')

        return XmlTree.tostring(self.root, encoding='unicode')

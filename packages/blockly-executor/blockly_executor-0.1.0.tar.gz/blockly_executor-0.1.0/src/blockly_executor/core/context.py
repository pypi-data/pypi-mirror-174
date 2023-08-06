from datetime import datetime
from blockly_executor import Helper, ArrayHelper
from blockly_executor.core.exceptions import LimitCommand


class Context:
    def __init__(self):
        self.protocol = None  # контекст операции

        self.data = {}
        # self.handler = {}
        self.params = {}  # параметры операции передающиеся между вызовами
        self.variables = {}  # значения переменных
        self.debug = {'__thread_vars': {}}  # контекст текущего блока, показывется при отладке
        self.operation = {}  # контекст операции
        self.deferred = []
        self.is_deferred = False
        self.deferred_result = None
        self.limit_commands = None
        self.connection = None

    def _init_from_dict(self, data):
        self.data = data.get('data', {})
        self.variables = data.get('var', {})
        self.debug = data.get('debug', {'__thread_vars': {}})
        self.operation = data.get('operation', {})
        self.deferred = data.get('deferred', [])

    @classmethod
    def init(cls, executor, *, protocol=None, data=None, params=None):
        # if not operation_id:
        #     operation_id = str(uuid4())
        self = cls()
        if not data:
            self.operation = dict(
                # globalBegin=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                commands=[],
                # comment='',
                status='run',
                # progress=-1,
                stepByStep=executor.step_by_step
            )
        else:
            self._init_from_dict(data)

        self.params = params if params else {}
        # self.operation = operation
        self.protocol = protocol

        self.operation['begin'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.set_limit(executor.step_by_step)
        return self

    def init_deferred(self, debug):
        _self = Context()
        _self.params = self.params
        _self.debug = debug['debug']
        _self.is_deferred = True
        _self.data = self.data
        _self.variables = self.variables
        _self.operation = self.operation
        _self.deferred = self.deferred
        _self.connection = self.connection
        return _self

    def init_nested(self, block_context):
        _self = Context()
        _self.params = self.params
        _self.debug = block_context.get('_context_debug', {})
        _self.is_deferred = True
        _self.data = self.data
        _self.variables = block_context.get('_context_variables', {})
        _self.operation = self.operation
        _self.deferred = self.deferred
        _self.connection = self.connection
        _self.set_limit()
        return _self

    def set_limit(self, step_by_step=False):
        self.limit_commands = 1 if step_by_step else 25

    @property
    def operation_id(self):
        return self.operation.get('operation_id')

    def to_parallel_dict(self):
        return dict(
            data=self.data,
            var=self.variables,
            debug=self.debug,
            operation=self.operation,
        )

    def to_dict(self):
        return dict(
            data=self.data,
            var=self.variables,
            debug=self.debug,
            operation=self.operation,
            deferred=self.deferred,
        )

    @staticmethod
    def get_child_context(block_context):
        try:
            child_context = block_context['__child']
        except KeyError:
            child_context = {}
            block_context['__child'] = child_context
        return child_context

    @staticmethod
    def clear_child_context(block_context, result=None, delete_children=True):
        if delete_children:
            block_context.pop('__child', None)

    def copy(self):
        _self = Context()
        _self.params = self.params
        _self.data = self.data
        _self.operation = self.operation
        _self.deferred = self.deferred
        _self.debug = Helper.copy_via_json(self.debug)
        # _self._init_from_dict(copy_via_json(self.to_dict()))
        return _self

    def add_deferred(self, deferred_exception):

        _local_context = deferred_exception.args[2]
        _operation_context = deferred_exception.args[1]
        try:
            i = ArrayHelper.find_by_key(self.deferred, _local_context['__deferred'], key_field='__deferred')
        except KeyError:
            self.deferred.append({})
            i = len(self.deferred) - 1

        self.deferred[i] = {
            '__deferred': _local_context['__deferred'],
            'debug': Helper.copy_via_json(_operation_context.debug)
        }

        try:
            i = ArrayHelper.find_by_key(self.operation['commands'], _local_context['__path'], key_field=2)
        except KeyError:
            self.operation['commands'].append([])
            i = len(self.operation['commands']) - 1
        self.operation['commands'][i] = deferred_exception.to_command()

    def check_command_limit(self):
        if len(self.operation['commands']) >= self.limit_commands:
            raise LimitCommand()

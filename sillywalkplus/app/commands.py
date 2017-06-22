import abc

from google.appengine.api.datastore_errors import BadRequestError

import models

commands_registery = []
commands_execution_by_variable = {}

class NoCommandsError(Exception):
    pass


class BaseCommand(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self, **item_specs):
        self.item_name = item_specs['item_name']

    @abc.abstractmethod
    def execute(self):
        pass

    def revert(self):
        commands_execution_by_variable[self.item_name].pop()
        try:
            revert_command = commands_execution_by_variable[self.item_name][-1]
            revert_command.execute()
        except IndexError:  # Reasoning - Regardless of whether we started from a SET or UNSET command, the previous command is implicitly UNSET.
            revert_command = UnsetCommand(item_name=self.item_name)
        revert_command.execute()

    @classmethod
    def create(cls, **kwargs):
        command = cls(**kwargs)
        commands_registery.append(command)
        try:
            commands_execution_by_variable[kwargs['item_name']].append(command)
        except KeyError:
            commands_execution_by_variable[kwargs['item_name']] = [command]
        return command


class SetItemCommand(BaseCommand):

    def __init__(self, **item_specs):
        super(SetItemCommand, self).__init__(**item_specs)
        self.item_value = item_specs['item_value']

    def execute(self):
        try:
            try:
                item = models.Item.get_by_id(self.item_name)
                if item.value != self.item_value:
                    models.ValueCount.decrement(item.value)
                    models.ValueCount.increment(self.item_value)
                    item.value = self.item_value
                    item.put()
            except AttributeError:
                item = models.Item(value=self.item_value, id=self.item_name)
                models.ValueCount.increment(self.item_value)
                item.put()
        except BadRequestError:
            no_op()

    def __repr__(self):
        return 'set(name={}, value={})'.format(self.item_name, self.item_value)


class UnsetCommand(BaseCommand):

    def __init__(self, **item_specs):
        super(UnsetCommand, self).__init__(**item_specs)
        self.item = models.Item.get_by_id(self.item_name)

    def execute(self):
        try:
            self.item.key.delete()
            models.ValueCount.decrement(self.item.value)
        except AttributeError:  # Already deleted.
            no_op()


    def __repr__(self):
        return 'unset(name={})'.format(self.item_name)


class EndCommand():

    def execute(self):
        global commands_registery
        global commands_execution_by_variable
        commands_registery = []
        commands_execution_by_variable = {}
        for item in models.Item.query():
            item.key.delete()
        for item in models.ValueCount.query():
            item.key.delete()


def undo_last_command():
    try:
        last_command = commands_registery.pop()
        last_command.revert()
    except IndexError:
        raise NoCommandsError()


def no_op():
    pass

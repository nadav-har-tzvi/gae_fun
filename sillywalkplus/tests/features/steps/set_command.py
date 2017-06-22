from behave import *
from app.models import ValueCount, Item
from app import commands

def convert_value(value):
    if value == 'NULL':
        return None
    else:
        return value

@given("A blank datastore")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    for vc in ValueCount.query():
        vc.key.delete()

    for item in Item.query():
        item.key.delete()


@when("Set command is invoked with {name} - {value}")
def step_impl(context, name, value):
    """
    :type context: behave.runner.Context
    :type name: str
    :type value: str
    """
    name = convert_value(name)
    value = convert_value(value)
    commands.SetItemCommand(item_name=name, item_value=value).execute()


@then("{name} should exist in the datastore")
def step_impl(context, name):
    """
    :type context: behave.runner.Context
    :type name: str
    """
    name = convert_value(name)
    item = Item.get_by_id(name)
    assert item is not None, "{} does not exist in the store!".format(name)


@step("{name} value in the store should be {value}")
def step_impl(context, name, value):
    """
    :type context: behave.runner.Context
    :type name: str
    :type value: str
    """
    name = convert_value(name)
    value = convert_value(value)
    item = Item.get_by_id(name)
    assert item.value == value, '{} value: {} != {}'.format(name, item.value, value)


@then("{name} should not exist in the datastore")
def step_impl(context, name):
    """
    :type context: behave.runner.Context
    :type name: str
    """
    name = convert_value(name)
    pass


@step("{name} should appear only once")
def step_impl(context, name):
    """
    :type context: behave.runner.Context
    :type name: str
    """
    name = convert_value(name)
    pass


@then("{value}'s count should be {expected_count:d}")
def step_impl(context, value, expected_count):
    """
    :type context: behave.runner.Context
    :type value: str
    """
    value = convert_value(value)
    vc = ValueCount.get_by_id(value)
    assert vc.count == expected_count, "{}'s count: {} != {}".format(value, vc.count, expected_count)
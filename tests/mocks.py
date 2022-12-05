import sys


def mock_open_todo_in_things(uuid):
    print(f'*** intercepted system command: open things:///show?id={uuid}')
    return 42


module = type(sys)('things_cli.thingsconnection')
module.open_todo_in_things = mock_open_todo_in_things
sys.modules['things_cli.thingsconnection'] = module

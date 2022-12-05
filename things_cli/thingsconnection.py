import os


def open_todo_in_things(uuid):
    return os.system(f'open things:///show?id={uuid}')

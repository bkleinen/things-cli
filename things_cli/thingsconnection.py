import os
FILE_NAME = "open_last.sh"


def open_todo_in_things(uuid):
    command = f'open things:///show?id={uuid}'
    _write_executable(command)
    print(f'opening todo. reopen it with ./{FILE_NAME}')
    return os.system(command)


def _write_executable(command):
    f = open(FILE_NAME, "w")
    f.write(command)
    f.close()
    os.chmod(file_name, 744)

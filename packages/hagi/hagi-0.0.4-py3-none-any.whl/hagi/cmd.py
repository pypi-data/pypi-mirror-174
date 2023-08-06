import os
import inspect
import importlib.util


from .task import Task
from .program import Program


def main():
    path = os.environ.get("HAGIPATH", "tasks.py")
    spec = importlib.util.spec_from_file_location('tasks', path)
    tasks = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tasks)

    program = Program(name='hagi')

    for key, value in inspect.getmembers(tasks):
        if isinstance(value, Task):
            program.add_task(value)
        elif key == 'program' and isinstance(value, Program):
            # "program" is a special variable name for cli call
            program = value
            break
    program.cmd()


if __name__ == '__main__':
    main()

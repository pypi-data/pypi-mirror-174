from __future__ import annotations
# Need Python 3.7 +

import inspect
import asyncio
from typing import List, Optional

import faba

from .task import Task


# TODO: add pre or post callable parameter
class Program:
    def __init__(self,
                 name: str,
                 desc: str = '',
                 ) -> None:
        self.name = name
        self.desc = desc
        self.sub_program = set()
        self.tasks = set()

    def add_task(self, obj: Task) -> None:
        if isinstance(obj, Task):
            self.tasks.add(obj)
        else:
            raise TypeError('only a Task instance can be added to Program')

    def add_program(self, obj: Program) -> None:
        self.sub_program.add(obj)

    def arg_parser(self) -> faba.Command:
        cmd = faba.Command(use=self.name + ' [Command]',
                           short=self.desc.split('\n')[0],
                           long=self.desc)
        for task in self.tasks:
            task_cmd = faba.Command(
                use=task.name + ' [Flags]',
                short=task.__doc__.strip().split('\n')[0],
                long=task.__doc__.strip(),
                run=self._run(task))

            for name, parameter in task._parameters():
                type = parameter.annotation if parameter.annotation is not inspect._empty else str
                default = parameter.default if parameter.default is not inspect._empty else None
                try:
                    task_cmd.add_flag('-' + name[0], '--' + name, type=type, default=default)
                except faba.exception.FlagError:
                    task_cmd.add_flag('--' + name, type=type, default=default)

            if task._ctx_type is not None:
                task_cmd.flags.merge(task._ctx_type.flags())

            cmd.add_command(task_cmd)

        for subp in self.sub_program:
            cmd.add_command(subp.arg_parser())

        return cmd

    def _run(self, task: Task):
        def runner(cmd: faba.Command, args: List[str]):
            params = {}
            for name, _ in task._parameters():
                params[name] = cmd.flags[name]

            if task._ctx_type is not None:
                ctx_flagset = faba.FlagSet()
                for flag in task._ctx_type.flags():
                    ctx_flagset.add_flag(cmd.flags.get_flag(flag.name))

                context = task._ctx_type(ctx_flagset, args)
                context.args = args
                asyncio.run(task(context, **params))
            else:
                asyncio.run(task(**params))

        return runner

    # TODO: change to async function
    def cmd(self, args: Optional[List[str]] = None) -> None:
        cmd = self.arg_parser()
        cmd.execute(args=args)

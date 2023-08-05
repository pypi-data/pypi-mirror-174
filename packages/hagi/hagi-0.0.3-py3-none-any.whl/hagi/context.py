from __future__ import annotations

import os

import asyncio
from typing import Dict, List, Callable, Iterable, Union
from contextlib import asynccontextmanager

import faba
from . import process
from .watcher import Watcher


class BasicContext:
    def __init__(self, flagset: faba.Flags = None, args: List[str] = []):
        # used to store additional args when running
        self.flagset = flagset
        self.args = args

    @classmethod
    def flags(cls) -> faba.FlagSet:
        return faba.FlagSet()


class Context(BasicContext):
    def __init__(self, flagset: faba.FlagSet, args: List[str] = []):
        super().__init__(flagset, args)
        self._cwd = os.getcwd()

    @asynccontextmanager
    async def cd(self, cwd: str) -> Context:
        nctx = self.__class__(self.flagset, self.args)
        nctx._cwd = cwd
        try:
            yield nctx
        finally:
            del nctx

    async def shell(self, cmd: str,
                    wait: bool = True,
                    watchers: Dict[str, Union[str, Iterable, Callable]] = {},
                    hide: bool = True,
                    pty: bool = False,
                    **kwargs) -> asyncio.subprocess.Process:
        watchers = [Watcher(pattern=p, response=r) for p, r in watchers.items()]

        if pty:
            kwargs['stdin'] = kwargs.get('stdin', process.PTY)
            kwargs['stdout'] = kwargs.get('stdout', process.PTY)
            kwargs['stderr'] = kwargs.get('stderr', process.PTY)
        else:
            kwargs['stdin'] = kwargs.get('stdin', process.PIPE)
            kwargs['stdout'] = kwargs.get('stdout', process.PIPE)
            kwargs['stderr'] = kwargs.get('stderr', process.PIPE)

        proc = await process.shell(cmd,
                                   hide=hide,
                                   watchers=watchers,
                                   loop=asyncio.get_running_loop(),
                                   cwd=self._cwd,
                                   **kwargs)
        if wait:
            await proc.wait()
        return proc

    async def exec(self,
                   *args,
                   wait: bool = True,
                   watchers: Dict[str, Union[str, Iterable, Callable]] = {},
                   hide: bool = True,
                   pty: bool = False,
                   **kwargs) -> asyncio.subprocess.Process:
        watchers = [Watcher(pattern=p, response=r) for p, r in watchers.items()]

        if pty:
            kwargs['stdin'] = kwargs.get('stdin', process.PTY)
            kwargs['stdout'] = kwargs.get('stdout', process.PTY)
            kwargs['stderr'] = kwargs.get('stderr', process.PTY)
        else:
            kwargs['stdin'] = kwargs.get('stdin', process.PIPE)
            kwargs['stdout'] = kwargs.get('stdout', process.PIPE)
            kwargs['stderr'] = kwargs.get('stderr', process.PIPE)

        proc = await process.exec(*args,
                                  hide=hide,
                                  watchers=watchers,
                                  loop=asyncio.get_running_loop(),
                                  cwd=self._cwd,
                                  **kwargs)
        if wait:
            await proc.wait()
        return proc

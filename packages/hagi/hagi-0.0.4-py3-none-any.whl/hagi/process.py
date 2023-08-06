from __future__ import annotations

import io
import re
import os
import sys
import pty
import fcntl
import shutil
import struct
import termios
import asyncio
import subprocess
from typing import List, Callable, Optional
from asyncio.base_subprocess import BaseSubprocessTransport, ReadSubprocessPipeProto, WriteSubprocessPipeProto

from .watcher import Watcher

PIPE = subprocess.PIPE
PTY = -100


class SubprocessRespondProtocol(asyncio.SubprocessProtocol):
    """
    Protocol for auto response
    Copy from asyncio.subprocess.SubprocessStreamProtocol
    """
    stdin: Optional[asyncio.StreamWriter]
    stdout: Optional[asyncio.StreamReader]
    stderr: Optional[asyncio.StreamReader]

    def __init__(self,
                 watchers: List[Watcher],
                 hide: bool,
                 limit: int = io.DEFAULT_BUFFER_SIZE):
        self._loop = asyncio.get_running_loop()
        self._limit = limit
        self._watchers = watchers
        self.hide = hide

        self.stdin = self.stdout = self.stderr = None

        self._buffer = (bytearray(), bytearray())
        self._process_exited = False
        self._pipe_fds: List[int] = []
        self._stdin_closed = self._loop.create_future()

    def connection_made(self, transport: asyncio.SubprocessTransport):  # type: ignore
        self._transport = transport
        stdout_transport = transport.get_pipe_transport(1)
        if stdout_transport is not None:
            self.stdout = asyncio.streams.StreamReader(limit=self._limit,
                                                       loop=self._loop)
            self.stdout.set_transport(stdout_transport)

        stderr_transport = transport.get_pipe_transport(2)
        if stderr_transport is not None:
            self.stderr = asyncio.streams.StreamReader(limit=self._limit,
                                                       loop=self._loop)
            self.stderr.set_transport(stderr_transport)

        stdin_transport: Optional[asyncio.WriteTransport] = transport.get_pipe_transport(0)  # type: ignore
        if stdin_transport is not None:
            self.stdin = asyncio.streams.StreamWriter(stdin_transport,
                                                      protocol=self,
                                                      reader=None,
                                                      loop=self._loop)

    def pipe_data_received(self, fd: int, data: bytes):
        buffer = None
        if fd == 1:
            buffer = self._buffer[0]
            reader = self.stdout
            self._pipe_fds.append(1)

        elif fd == 2:
            buffer = self._buffer[1]
            reader = self.stderr
            self._pipe_fds.append(2)
        else:
            reader = None
        if reader is not None and not reader.at_eof():
            reader.feed_data(data)

        if not self.hide and fd == 1:
            sys.stdout.buffer.write(data)
        if not self.hide and fd == 2:
            sys.stderr.buffer.write(data)

        if buffer is not None and self.stdin is not None:
            buffer.extend(data)
            for watcher in self._watchers:
                match = re.search(watcher.pattern, buffer[watcher.start:])
                if match is not None:
                    watcher.start += match.end()
                    responde = watcher.response(match)
                    if not self.stdin.is_closing():
                        self.stdin.write(responde)

    def pipe_connection_lost(self, fd, exc):
        if fd == 0:
            pipe = self.stdin
            if pipe is not None:
                pipe.close()
            self.connection_lost(exc)
            if exc is None:
                self._stdin_closed.set_result(None)
            else:
                self._stdin_closed.set_exception(exc)
            return
        if fd == 1:
            reader = self.stdout
        elif fd == 2:
            reader = self.stderr
        else:
            reader = None
        if reader is not None:
            if exc is None:
                reader.feed_eof()
            else:
                reader.set_exception(exc)

        if fd in self._pipe_fds:
            self._pipe_fds.remove(fd)
        self._maybe_close_transport()

    def process_exited(self):
        self._process_exited = True
        self._maybe_close_transport()

    def _maybe_close_transport(self):
        if len(self._pipe_fds) == 0 and self._process_exited:
            self._transport.close()
            self._transport = None

    @classmethod
    def factory(cls, watchers: List[Watcher] = [],
                hide: bool = True,
                limit: int = io.DEFAULT_BUFFER_SIZE) -> Callable[[], SubprocessRespondProtocol]:
        def wrapped() -> SubprocessRespondProtocol:
            return cls(watchers=watchers, limit=limit, hide=hide)

        return wrapped


class PTYTransport(BaseSubprocessTransport):
    def __init__(self, *args, **kwargs):
        self._pty_fd = None
        self._pty_pipe = [None, None, None]
        super().__init__(*args, **kwargs)

    def _start(self, args, shell, stdin, stdout, stderr, bufsize, **kwargs):

        if any([i == PTY for i in (stdin, stdout, stderr)]):
            master_fd, slave_fd = pty.openpty()
            self._pty_fd = master_fd

            # TODO: Change default size
            tsize = shutil.get_terminal_size(fallback=(480, 360))
            self.resize_pty(tsize.columns, tsize.lines)
            if stdin == PTY:
                stdin = slave_fd
                self._pty_pipe[0] = open(master_fd, 'wb', closefd=False)
            if stdout == PTY:
                stdout = slave_fd
                self._pty_pipe[1] = open(master_fd, 'rb', closefd=False)
            if stderr == PTY:
                err_master_fd, err_slave_fd = pty.openpty()
                stderr = err_slave_fd
                self._pty_pipe[2] = open(err_master_fd, 'rb', closefd=False)

        self._proc = subprocess.Popen(
            args, shell=shell, stdin=stdin, stdout=stdout, stderr=stderr,
            universal_newlines=False, bufsize=bufsize, **kwargs)

    # rewrite BaseSubprocessTransport._connect_pipes
    async def _connect_pipes(self, waiter):
        try:
            proc = self._proc
            loop = self._loop

            if proc.stdin is not None:
                _, pipe = await loop.connect_write_pipe(
                    lambda: WriteSubprocessPipeProto(self, 0),
                    proc.stdin)
                self._pipes[0] = pipe
            elif self._pty_pipe[0] is not None:
                _, pipe = await loop.connect_write_pipe(
                    lambda: WriteSubprocessPipeProto(self, 0),
                    self._pty_pipe[0])
                self._pipes[0] = pipe

            if proc.stdout is not None:
                _, pipe = await loop.connect_read_pipe(
                    lambda: ReadSubprocessPipeProto(self, 1),
                    proc.stdout)
                self._pipes[1] = pipe
            elif self._pty_pipe[1] is not None:
                _, pipe = await loop.connect_read_pipe(
                    lambda: ReadSubprocessPipeProto(self, 1),
                    self._pty_pipe[1])
                self._pipes[1] = pipe

            if proc.stderr is not None:
                _, pipe = await loop.connect_read_pipe(
                    lambda: ReadSubprocessPipeProto(self, 2),
                    proc.stderr)
                self._pipes[2] = pipe
            elif self._pty_pipe[2] is not None:
                _, pipe = await loop.connect_read_pipe(
                    lambda: ReadSubprocessPipeProto(self, 2),
                    self._pty_pipe[2])
                self._pipes[2] = pipe

            assert self._pending_calls is not None

            loop.call_soon(self._protocol.connection_made, self)
            for callback, data in self._pending_calls:
                loop.call_soon(callback, *data)
            self._pending_calls = None
        except (SystemExit, KeyboardInterrupt):
            raise
        except BaseException as exc:
            if waiter is not None and not waiter.cancelled():
                waiter.set_exception(exc)
        else:
            if waiter is not None and not waiter.cancelled():
                waiter.set_result(None)

    def __del__(self, *args, **kwargs):
        if self._pty_fd is not None:
            os.close(self._pty_fd)
        super().__del__(*args, **kwargs)

    def resize_pty(self, columns: int, lines: int):
        winsize = struct.pack("HHHH", lines, columns, 0, 0)
        fcntl.ioctl(self._pty_fd, termios.TIOCSWINSZ, winsize)


async def _make_potransport(
        loop: asyncio.AbstractEventLoop, protocol,
        args, shell, stdin, stdout, stderr, bufsize,
        extra=None, **kwargs):
    with asyncio.get_child_watcher() as watcher:
        waiter = loop.create_future()

        transp = PTYTransport(loop, protocol, args, shell,
                              stdin, stdout, stderr, bufsize,
                              waiter=waiter, extra=extra,
                              **kwargs)

        def _child_watcher_callback(pid, returncode, transp):
            # Skip one iteration for callbacks to be executed
            loop.call_soon_threadsafe(loop.call_soon, transp._process_exited, returncode)

        watcher.add_child_handler(transp.get_pid(),  # type: ignore
                                  _child_watcher_callback, transp)
        try:
            await waiter
        except (SystemExit, KeyboardInterrupt):
            raise
        except BaseException:
            transp.close()
            await transp._wait()
            raise

    return transp


async def _exec(loop, protocol_factory, program, *args,
                stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, universal_newlines=False,
                shell=False, bufsize=0,
                encoding=None, errors=None, text=None,
                **kwargs):
    if universal_newlines:
        raise ValueError("universal_newlines must be False")
    if shell:
        raise ValueError("shell must be False")
    if bufsize != 0:
        raise ValueError("bufsize must be 0")
    if text:
        raise ValueError("text must be False")
    if encoding is not None:
        raise ValueError("encoding must be None")
    if errors is not None:
        raise ValueError("errors must be None")

    popen_args = (program,) + args
    protocol = protocol_factory()
    transport = await _make_potransport(
        loop, protocol,
        popen_args, False, stdin, stdout, stderr, bufsize,
        **kwargs)
    return transport, protocol


async def exec(*args,
               hide: bool = True,
               watchers: List[Watcher] = [],
               loop=None,
               **kwargs) -> asyncio.subprocess.Process:
    loop = asyncio.get_running_loop() if loop is None else loop
    transport, protocol = await _exec(
        loop, SubprocessRespondProtocol.factory(hide=hide, watchers=watchers),
        *args,
        **kwargs
    )
    proc = asyncio.subprocess.Process(transport, protocol, loop)
    return proc


async def _shell(loop, protocol_factory, cmd, *,
                 stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                 stderr=subprocess.PIPE, universal_newlines=False,
                 shell=True, bufsize=0,
                 encoding=None, errors=None, text=None,
                 **kwargs):
    if not isinstance(cmd, (bytes, str)):
        raise ValueError("cmd must be a string")
    if universal_newlines:
        raise ValueError("universal_newlines must be False")
    if not shell:
        raise ValueError("shell must be True")
    if bufsize != 0:
        raise ValueError("bufsize must be 0")
    if text:
        raise ValueError("text must be False")
    if encoding is not None:
        raise ValueError("encoding must be None")
    if errors is not None:
        raise ValueError("errors must be None")

    protocol = protocol_factory()

    transport = await _make_potransport(
        loop, protocol,
        cmd, True, stdin, stdout, stderr, bufsize,
        **kwargs)

    return transport, protocol


async def shell(cmd: str, hide: bool = True,
                watchers: List[Watcher] = [],
                loop=None,
                *args, **kwargs) -> asyncio.subprocess.Process:
    loop = asyncio.get_running_loop() if loop is None else loop
    transport, protocol = await _shell(
        loop,
        SubprocessRespondProtocol.factory(hide=hide, watchers=watchers),
        cmd,
        *args,
        **kwargs
    )
    proc = asyncio.subprocess.Process(transport, protocol, loop)
    return proc

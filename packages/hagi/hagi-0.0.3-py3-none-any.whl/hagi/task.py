from __future__ import annotations

import inspect
import functools
from typing import Callable, Any, Type, Optional

from .context import Context, BasicContext


class Task:
    def __init__(
            self,
            body: Callable,
            name: str = None,
    ) -> None:

        self.__doc__ = getattr(body, "__doc__", "")
        self.__doc__ = '' if self.__doc__ is None else self.__doc__

        self.__name__ = getattr(body, "__name__", "")
        self.__module__ = getattr(body, "__module__", "")

        if not inspect.iscoroutinefunction(body):
            raise TypeError('task body must be a coroutine')
        self.body = body
        self.name = name or self.__name__

    async def __call__(self, *args, **kwargs) -> Any:
        return await self.body(*args, **kwargs)

    def _parameters(self):
        params = list(inspect.signature(self.body).parameters.items())
        if self._ctx_type is not None:
            params = params[1:]

        for name, param in params:
            if param.kind != param.VAR_KEYWORD and param.kind != param.VAR_POSITIONAL:
                yield (name, param)
            else:
                continue

        return

    """
    only works for python >= 3.8
    use
    @property
    @functools.lru_cache()

    for backport, write self decoration
    """
    @functools.cached_property
    def _ctx_type(self) -> Optional[Type[BasicContext]]:
        parameters = list(inspect.signature(self.body).parameters.items())
        if len(parameters) < 1:
            return None
        elif parameters[0][1].annotation is inspect._empty:
            return Context
        elif not inspect.isclass(parameters[0][1].annotation):
            return None
        elif issubclass(parameters[0][1].annotation, BasicContext):
            return parameters[0][1].annotation
        else:
            return None


def task(*args, **kwargs) -> Task:
    klass = kwargs.pop("klass", Task)

    if len(args) == 1 and callable(args[0]) and not isinstance(args[0], Task):
        return klass(args[0], **kwargs)

    name = kwargs.pop("name", None)

    def inner_decrotator(obj):
        obj = klass(
            obj,
            name=name,
            **kwargs
        )
        return obj

    return inner_decrotator

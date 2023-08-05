import re
from typing import Union, Iterable, Callable


class Watcher:
    def __init__(self,
                 pattern: Union[str, bytes],
                 response: Union[str, bytes, Iterable, Callable[[re.Match], bytes]],
                 ):
        self.pattern = pattern.encode() if isinstance(pattern, str) else pattern
        if isinstance(response, str):
            self._response = response.encode()
        elif isinstance(response, bytes) or isinstance(response, bytearray):
            self._response = response
        elif isinstance(response, Iterable):
            # be careful, string and bytes, bytearray is iterable too
            self._response = iter(response)
        else:
            self._response = response

        self.start = 0

    def __repr__(self):
        return (f'<hagi.Watcher pattern "{self.pattern.decode()}" '
                f'response "{self.response.decode()}" '
                f'start at {self.start}>')

    def response(self, matched: re.Match) -> bytes:
        if isinstance(self._response, bytes):
            return self._response
        elif isinstance(self._response, Iterable):
            try:
                r = next(self._response)
                r = r.encode() if isinstance(r, str) else r
            except StopIteration:
                r = b''
            finally:
                return r
        elif isinstance(self._response, Callable):
            r = self._response(matched)
            r = r.encode() if isinstance(r, str) else r
            return r
        else:
            raise ValueError("invalid response type")

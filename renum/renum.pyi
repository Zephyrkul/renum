from __future__ import annotations

from contextvars import ContextVar
from enum import Enum, EnumMeta
from typing import Any, Iterator
from typing_extensions import Self

import regex

__all__ = ("RenumType", "renum")
_matches: ContextVar[dict[renum, regex.Match[str]]] = ContextVar("_match")

class RenumType(EnumMeta):
    """Metaclass for renum classes"""

    _pattern_: regex.Pattern[str]

    @property
    def pattern(self) -> regex.Pattern[str]: ...

class renum(Enum, metaclass=RenumType):
    """
    A utility class for generating Enum-like regular expression patterns.

    Parameters:
        flags (int | re.RegexFlag): Regular expression flags to pass to `re.compile`
    """

    _value_: str

    @property
    def value(self) -> str: ...
    @property
    def last_match(self) -> regex.Match[str] | Any: ...
    @classmethod
    def search(
        cls,
        string: str,
        pos: int = ...,
        endpos: int = ...,
        concurrent: bool | None = ...,
        timeout: float | None = ...,
    ) -> Self | None: ...
    @classmethod
    def match(
        cls,
        string: str,
        pos: int = ...,
        endpos: int = ...,
        concurrent: bool | None = ...,
        timeout: float | None = ...,
    ) -> Self | None: ...
    @classmethod
    def fullmatch(
        cls,
        string: str,
        pos: int = ...,
        endpos: int = ...,
        concurrent: bool | None = ...,
        timeout: float | None = ...,
    ) -> Self | None: ...
    @classmethod
    def findall(
        cls,
        string: str,
        pos: int = ...,
        endpos: int = ...,
        overlapped: bool = ...,
        concurrent: bool | None = ...,
        timeout: float | None = ...,
    ) -> list[Self]: ...
    @classmethod
    def finditer(
        cls,
        string: str,
        pos: int = ...,
        endpos: int = ...,
        overlapped: bool = ...,
        concurrent: bool | None = ...,
        timeout: float | None = ...,
    ) -> Iterator[Self]: ...

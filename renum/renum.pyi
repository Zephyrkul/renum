from __future__ import annotations

from enum import Enum, EnumMeta
from typing import Any, Iterator
from typing_extensions import Self

import regex

__all__ = ("RenumType", "renum")

class RenumType(EnumMeta):
    @property
    def pattern(self) -> regex.Pattern[str]: ...

class renum(Enum, metaclass=RenumType):
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

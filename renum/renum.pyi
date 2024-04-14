from enum import Enum, EnumMeta, _EnumDict  # type: ignore[reportPrivateUsage]
from typing import Any, overload
from typing_extensions import Buffer, Self

import regex
from regex._regex import Scanner

__all__ = ("RenumType", "renum")

class _Scanner[renum: renum](Scanner[str]):  # type: ignore
    def __iter__(self) -> Self: ...
    def __next__(self) -> renum: ...
    def match(self) -> renum | None: ...
    def search(self) -> renum | None: ...

class RenumType(EnumMeta, regex.Pattern[str]):  # type: ignore
    # flags is actually implemented in __init_subclass__,
    # but pyright doesn't pick up on that
    def __new__[RenumTypeT: RenumType](
        metacls: type[RenumTypeT],
        cls: str,
        bases: tuple[type, ...],
        classdict: _EnumDict,
        *,
        flags: int | regex.RegexFlag = ...,
        **kwds: Any,
    ) -> RenumTypeT: ...

    _pattern_: regex.Pattern[str]

    def search[renumT: renum](
        cls: type[renumT],
        string: str,
        pos: int = ...,
        endpos: int = ...,
        concurrent: bool | None = ...,
        timeout: float | None = ...,
    ) -> renumT | None:
        """
        Searches the specified string for an instance of this renum class,
        as per the `regex.Pattern.search` method.
        """

    def match[renumT: renum](
        cls: type[renumT],
        string: str,
        pos: int = ...,
        endpos: int = ...,
        concurrent: bool | None = ...,
        timeout: float | None = ...,
    ) -> renumT | None:
        """
        Searches the specified string for an instance of this renum class,
        as per the `regex.Pattern.match` method.
        """

    def fullmatch[renumT: renum](
        cls: type[renumT],
        string: str,
        pos: int = ...,
        endpos: int = ...,
        concurrent: bool | None = ...,
        timeout: float | None = ...,
    ) -> renumT | None:
        """
        Searches the specified string for an instance of this renum class,
        as per the `regex.Pattern.fullmatch` method.
        """

    def finditer[renumT: renum](
        cls: type[renumT],
        string: str,
        pos: int = ...,
        endpos: int = ...,
        overlapped: bool = ...,
        concurrent: bool | None = ...,
        timeout: float | None = ...,
    ) -> _Scanner[renumT]:
        """
        Searches the specified string for instances of this renum class,
        as per the `regex.Pattern.finditer` method.
        """

    def scanner[renumT: renum](
        cls: type[renumT],
        string: str,
        pos: int | None = ...,
        endpos: int | None = ...,
        overlapped: bool = ...,
        concurrent: bool | None = ...,
        timeout: float | None = ...,
    ) -> _Scanner[renumT]:
        """
        Searches the specified string for instances of this renum class,
        as per the `regex.Pattern.scanner` method.
        """

class renum(Enum, regex.Match[str], metaclass=RenumType):  # type: ignore
    _value_: str
    @overload
    def __new__(cls, value: str = ..., /) -> Self: ...
    @overload
    def __new__(cls, value: Buffer, encoding: str, errors: str = ..., /) -> Self: ...
    @property
    def last_match(self) -> regex.Match[str] | Any:
        """
        The last `regex.Match` that matched this renum member's pattern, if any.
        """

# the below regex subclassing is a white lie to make typechecking easier

from enum import Enum, EnumMeta, _EnumDict  # type: ignore[reportPrivateUsage]
from typing import Any, overload
from typing_extensions import Buffer, Self, override

import regex
from regex._regex import Scanner

__all__ = ("RenumType", "renum")

class _Scanner[_renumT: renum](Scanner[str]):  # type: ignore
    @override
    def __iter__(self) -> Self: ...
    @override
    def __next__(self) -> _renumT: ...
    @override
    def match(self) -> _renumT | None: ...
    @override
    def search(self) -> _renumT | None: ...

class RenumType(EnumMeta, regex.Pattern[str]):  # type: ignore
    """Metaclass for renum classes"""

    # flags is actually implemented in __init_subclass__,
    # but pyright doesn't pick up on that
    def __new__[_RenumTypeT: RenumType](
        metacls: type[_RenumTypeT],
        cls: str,
        bases: tuple[type, ...],
        classdict: _EnumDict,
        *,
        flags: int | regex.RegexFlag = ...,
        **kwds: Any,
    ) -> _RenumTypeT: ...

    _pattern_: regex.Pattern[str]

    @override
    def search[_renumT: renum](
        cls: type[_renumT],
        string: str,
        pos: int = ...,
        endpos: int = ...,
        concurrent: bool | None = ...,
        timeout: float | None = ...,
    ) -> _renumT | None:
        """
        Searches the specified string for an instance of this renum class,
        as per the `regex.Pattern.search` method.
        """

    @override
    def match[_renumT: renum](
        cls: type[_renumT],
        string: str,
        pos: int = ...,
        endpos: int = ...,
        concurrent: bool | None = ...,
        timeout: float | None = ...,
    ) -> _renumT | None:
        """
        Searches the specified string for an instance of this renum class,
        as per the `regex.Pattern.match` method.
        """

    @override
    def fullmatch[_renumT: renum](
        cls: type[_renumT],
        string: str,
        pos: int = ...,
        endpos: int = ...,
        concurrent: bool | None = ...,
        timeout: float | None = ...,
    ) -> _renumT | None:
        """
        Searches the specified string for an instance of this renum class,
        as per the `regex.Pattern.fullmatch` method.
        """

    @override
    def finditer[_renumT: renum](
        cls: type[_renumT],
        string: str,
        pos: int = ...,
        endpos: int = ...,
        overlapped: bool = ...,
        concurrent: bool | None = ...,
        timeout: float | None = ...,
    ) -> _Scanner[_renumT]:
        """
        Searches the specified string for instances of this renum class,
        as per the `regex.Pattern.finditer` method.
        """

    @override
    def scanner[_renumT: renum](
        cls: type[_renumT],
        string: str,
        pos: int | None = ...,
        endpos: int | None = ...,
        overlapped: bool = ...,
        concurrent: bool | None = ...,
        timeout: float | None = ...,
    ) -> _Scanner[_renumT]:
        """
        Searches the specified string for instances of this renum class,
        as per the `regex.Pattern.scanner` method.
        """

class renum(Enum, regex.Match[str], metaclass=RenumType):  # type: ignore
    """
    A utility class for generating Enum-like regular expression patterns.

    Parameters:
        flags (int | regex.RegexFlag): Regular expression flags to pass to `regex.compile`
    """

    _value_: str

    @overload
    def __new__(cls, value: str = ..., /) -> Self: ...
    @overload
    def __new__(cls, value: Buffer, encoding: str, errors: str = ..., /) -> Self: ...

    # Actual return type is -> regex.Match[str] | None
    # In most cases when this is used, a match has statically been made
    @property
    def last_match(self) -> regex.Match[str] | Any:
        """
        The last `regex.Match` that matched this renum member's pattern, if any.
        """

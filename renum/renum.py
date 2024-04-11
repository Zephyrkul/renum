from __future__ import annotations

import re
import sys
from contextvars import ContextVar
from enum import Enum
from typing import TYPE_CHECKING, Any, Iterator, overload

if TYPE_CHECKING:
    from typing_extensions import Self


__all__ = ("renum",)
_matches: ContextVar[dict[renum, re.Match[str]]] = ContextVar("_match")


class renum(Enum):
    if TYPE_CHECKING:
        _pattern_: re.Pattern[str]
        _value_: str

        @property
        def value(self) -> str: ...

    @staticmethod
    def _generate_next_value_(
        name: str, start: int, count: int, last_values: list[str]
    ) -> str:
        raise TypeError("enum.auto() used with renum")

    def __new__(cls, *values: Any) -> Self:
        value = str(*values)
        member = object.__new__(cls)
        member._value_ = value
        return member

    def __init_subclass__(cls, flags: int | re.RegexFlag = 0, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        cls._pattern_ = re.compile(
            r"|".join(rf"(?P<{member.name}>{member.value})" for member in cls),
            flags=flags,
        )

    def __str__(self) -> str:
        return self.value

    __hash__ = object.__hash__

    @property
    def last_match(self) -> re.Match[str] | None:
        """
        The last re.Match that matched this renum member's pattern.
        """
        return _matches.get({}).get(self)

    @property
    def pattern(self) -> re.Pattern[str]:
        """
        The compiled re.Pattern for this renum class.
        """
        return self.__class__._pattern_

    @overload
    @classmethod
    def _from_match(cls, match: None) -> None: ...
    @overload
    @classmethod
    def _from_match(cls, match: re.Match[str]) -> Self: ...

    @classmethod
    def _from_match(cls, match: re.Match[str] | None) -> Self | None:
        if not match:
            return None
        matched_groups = match.groupdict()
        self = next(member for member in cls if matched_groups[member.name] is not None)
        matches = _matches.get({})
        matches[self] = match
        _matches.set(matches)
        return self

    @classmethod
    def search(
        cls, string: str, pos: int = 0, endpos: int = sys.maxsize
    ) -> Self | None:
        """
        Searches the specified string for an instance of this renum class,
        as per the standard lib's re.search function.
        """
        return cls._from_match(cls._pattern_.search(string, pos, endpos))

    @classmethod
    def match(cls, string: str, pos: int = 0, endpos: int = sys.maxsize) -> Self | None:
        """
        Searches the specified string for an instance of this renum class,
        as per the standard lib's re.match function.
        """
        return cls._from_match(cls._pattern_.match(string, pos, endpos))

    @classmethod
    def fullmatch(
        cls, string: str, pos: int = 0, endpos: int = sys.maxsize
    ) -> Self | None:
        """
        Searches the specified string for an instance of this renum class,
        as per the standard lib's re.fullmatch function.
        """
        return cls._from_match(cls._pattern_.fullmatch(string, pos, endpos))

    @classmethod
    def findall(
        cls, string: str, pos: int = 0, endpos: int = sys.maxsize
    ) -> list[Self]:
        """
        Searches the specified string for all instances of this renum class,
        as per the standard lib's re.findall function.
        """
        return list(cls.finditer(string, pos, endpos))

    @classmethod
    def finditer(
        cls, string: str, pos: int = 0, endpos: int = sys.maxsize
    ) -> Iterator[Self]:
        """
        Searches the specified string for instances of this renum class,
        as per the standard lib's re.finditer function.
        """
        return map(cls._from_match, cls._pattern_.finditer(string, pos, endpos))

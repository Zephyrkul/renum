from __future__ import annotations

from contextvars import ContextVar
from enum import Enum, EnumMeta
from typing import TYPE_CHECKING, Any, Iterator, overload

import regex

if TYPE_CHECKING:
    from typing_extensions import Never, Self


__all__ = ("RenumType", "renum")
_matches: ContextVar[dict[renum, regex.Match[str]]] = ContextVar("_match")


class RenumType(EnumMeta):
    """Metaclass for renum classes"""

    _pattern_: regex.Pattern[str]

    @property
    def pattern(self) -> regex.Pattern[str]:
        """
        The compiled `re.Pattern` for this renum class.
        """
        return self._pattern_


class renum(Enum, metaclass=RenumType):
    """
    A utility class for generating Enum-like regular expression patterns.

    Parameters:
        flags (int | re.RegexFlag): Regular expression flags to pass to `re.compile`
    """

    @staticmethod
    def _generate_next_value_(
        name: str, start: int, count: int, last_values: list[str]
    ) -> Never:
        raise TypeError("enum.auto() used with renum")

    def __new__(cls, *values: Any) -> Self:
        value = str(*values)
        member = object.__new__(cls)
        member._value_ = value
        return member

    def __init_subclass__(cls, flags: int | regex.RegexFlag = 0, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        cls._pattern_ = regex.compile(  # type: ignore[reportPrivateUsage]
            r"|".join(rf"(?P<{member.name}>{member.value})" for member in cls),
            flags=flags,
        )

    def __str__(self) -> str:
        return self.value

    __hash__ = object.__hash__

    @property
    def last_match(self) -> regex.Match[str] | Any:
        """
        The last `regex.Match` that matched this renum member's pattern.
        """
        return _matches.get({}).get(self)

    @overload
    @classmethod
    def _from_match(cls, match: None) -> None: ...
    @overload
    @classmethod
    def _from_match(cls, match: regex.Match[str]) -> Self: ...

    @classmethod
    def _from_match(cls, match: regex.Match[str] | None) -> Self | None:
        if not match:
            return None
        matched_groups = match.groupdict()
        self = next(member for member in cls if matched_groups[member.name] is not None)
        matches = _matches.get({})
        matches[self] = match
        _matches.set(matches)
        return self

    @classmethod
    def search(cls, *args: Any, **kwargs: Any) -> Self | None:
        """
        Searches the specified string for an instance of this renum class,
        as per the `regex.Pattern.search` method.
        """
        return cls._from_match(cls.pattern.search(*args, **kwargs))

    @classmethod
    def match(cls, *args: Any, **kwargs: Any) -> Self | None:
        """
        Searches the specified string for an instance of this renum class,
        as per the `regex.Pattern.match` method.
        """
        return cls._from_match(cls.pattern.match(*args, **kwargs))

    @classmethod
    def fullmatch(cls, *args: Any, **kwargs: Any) -> Self | None:
        """
        Searches the specified string for an instance of this renum class,
        as per the `regex.Pattern.fullmatch` method.
        """
        return cls._from_match(cls.pattern.fullmatch(*args, **kwargs))

    @classmethod
    def findall(cls, *args: Any, **kwargs: Any) -> list[Self]:
        """
        Searches the specified string for all instances of this renum class,
        as per the `regex.Pattern.findall` method.
        """
        return list(cls.finditer(*args, **kwargs))

    @classmethod
    def finditer(cls, *args: Any, **kwargs: Any) -> Iterator[Self]:
        """
        Searches the specified string for instances of this renum class,
        as per the `regex.Pattern.finditer` method.
        """
        return map(cls._from_match, cls.pattern.finditer(*args, **kwargs))

from __future__ import annotations

from contextvars import ContextVar
from enum import Enum, EnumMeta
from typing import TYPE_CHECKING, Any, Generic, TypeVar, cast, overload

import regex

if TYPE_CHECKING:
    from typing_extensions import Never, Self

    from regex._regex import Scanner


__all__ = ("RenumType", "renum")
_renumT = TypeVar("_renumT", bound="renum")
_matches: ContextVar[dict[renum, regex.Match[str]]] = ContextVar("_match")


if TYPE_CHECKING:
    # typeshed is missing attributes for regex.error
    class _error(regex.error):
        msg: str
        pattern: str | None
        pos: int | None
        lineno: int
        colno: int


class _Scanner(Generic[_renumT]):
    __slots__ = ("_func", "_scanner")

    def __init__(self, f: Any, scanner: Scanner[str]) -> None:
        self._func = f
        self._scanner = scanner

    def __iter__(self):
        return self

    def __next__(self) -> _renumT:
        return self._func(next(self._scanner))

    def __getattr__(self, name: str) -> Any:
        return getattr(self._scanner, name)

    def match(self) -> _renumT | None:
        return self._func(self._scanner.match())

    def search(self) -> _renumT | None:
        return self._func(self._scanner.search())


def _augment_error(err: regex.error, name: str) -> None:
    # attaches some debugging info to the error message
    err = cast("_error", err)
    if err.pattern is None or err.pos is None:
        return
    (message,) = err.args
    line = err.pattern.split("\n")[err.lineno - 1]
    message = f"{message} in {name}\n{line}\n{'^'.rjust(err.colno)}"
    err.args = (message,)


class RenumType(EnumMeta):
    """Metaclass for renum classes"""

    # default to never matching anything
    _pattern_: regex.Pattern[str] = regex.compile(r"^\b$")

    @overload
    def _from_match(cls, match: None) -> None: ...
    @overload
    def _from_match(cls: type[_renumT], match: regex.Match[str]) -> _renumT: ...

    def _from_match(
        cls: type[_renumT], match: regex.Match[str] | None
    ) -> _renumT | None:
        if not match:
            return None
        matched_groups = match.groupdict()
        self = next(member for member in cls if matched_groups[member.name] is not None)
        matches = _matches.get({})
        matches[self] = match
        _matches.set(matches)
        return self

    def search(cls: type[_renumT], *args: Any, **kwargs: Any) -> _renumT | None:
        """
        Searches the specified string for an instance of this renum class,
        as per the `regex.Pattern.search` method.
        """
        return cls._from_match(cls._pattern_.search(*args, **kwargs))

    def match(cls: type[_renumT], *args: Any, **kwargs: Any) -> _renumT | None:
        """
        Searches the specified string for an instance of this renum class,
        as per the `regex.Pattern.match` method.
        """
        return cls._from_match(cls._pattern_.match(*args, **kwargs))

    def fullmatch(cls: type[_renumT], *args: Any, **kwargs: Any) -> _renumT | None:
        """
        Searches the specified string for an instance of this renum class,
        as per the `regex.Pattern.fullmatch` method.
        """
        return cls._from_match(cls._pattern_.fullmatch(*args, **kwargs))

    def finditer(cls: type[_renumT], *args: Any, **kwargs: Any) -> _Scanner[_renumT]:
        """
        Searches the specified string for instances of this renum class,
        as per the `regex.Pattern.finditer` method.
        """
        return _Scanner(cls._from_match, cls._pattern_.finditer(*args, **kwargs))

    def scanner(cls: type[_renumT], *args: Any, **kwargs: Any) -> _Scanner[_renumT]:
        """
        Scans the specified string for instances of this renum class,
        as per the `regex.Pattern.scanner` method.
        """
        return _Scanner(cls._from_match, cls._pattern_.scanner(*args, **kwargs))

    def __getattr__(cls, name: str) -> Any:
        return getattr(cls._pattern_, name)


class renum(Enum, metaclass=RenumType):
    """
    A utility class for generating Enum-like regular expression patterns.

    Parameters:
        flags (int | regex.RegexFlag): Regular expression flags to pass to `regex.compile`
    """

    @staticmethod
    def _generate_next_value_(
        name: str, start: int, count: int, last_values: list[str]
    ) -> Never:
        raise TypeError("enum.auto() used with renum")

    def __new__(cls, value: object, /, *args: Any) -> Self:
        if not args and type(value) is not str:  # noqa: E721
            raise TypeError(f"renum values must be str, not {type(value).__qualname__}")
        value = str(value, *args)
        member = object.__new__(cls)
        member._value_ = value
        return member

    def __init_subclass__(
        cls, flags: int | regex.RegexFlag = 0, **keywords: Any
    ) -> None:
        super().__init_subclass__(**keywords)
        if not len(cls):
            return  # use the default null-match pattern
        debug = flags & regex.DEBUG != 0
        if debug:
            cls._debug_instances(flags)
        flags = flags & ~regex.DEBUG
        try:
            cls._pattern_ = regex.compile(  # type: ignore[reportPrivateUsage]
                "|".join(f"(?P<{member.name}>{member.value})" for member in cls),
                flags=flags,
            )
        except regex.error as err:
            if not debug:
                cls._debug_instances(flags)
            # somehow each member compiles but renum doesn't
            _augment_error(err, cls.__qualname__)
            raise AssertionError from err

    @classmethod
    def _debug_instances(cls, flags: int | regex.RegexFlag):
        # try to find the problematic regex
        for member in cls:
            try:
                regex.compile(member.value, flags=flags, cache_pattern=False)
            except regex.error as err:
                # found it
                # attach some extra info
                _augment_error(err, member.name)
                raise

    def __str__(self) -> str:
        return self.value

    __hash__ = object.__hash__

    @property
    def last_match(self) -> regex.Match[str] | Any:
        """
        The last `regex.Match` that matched this renum member's pattern, if any.
        """
        return _matches.get({}).get(self)

    def __getattr__(self, name: str) -> Any:
        last_match = self.last_match
        if last_match is None:
            raise RuntimeError(
                f"renum {type(self).__qualname__}.{self.name} has"
                " yet to match any string in the current context"
            )
        return getattr(self.last_match, name)

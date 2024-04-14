# renum

[![pypi](https://img.shields.io/pypi/v/renum.svg)](https://pypi.org/project/renum/)
[![Licensed under the MIT License](https://img.shields.io/pypi/l/renum.svg)](https://choosealicense.com/licenses/mit/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/Zephyrkul/sans/master.svg)](https://results.pre-commit.ci/latest/github/Zephyrkul/sans/master)

**Re**gex E**num**

A utility class for generating [Enum](https://docs.python.org/3/library/enum.html#enum.Enum)-like regular expression patterns.

## Installing

```sh
python3 -m pip install -U renum
```

Development version:

```sh
python3 -m pip install -U https://github.com/Zephyrkul/renum/archive/master.zip#egg=renum
```

## Support

If you need help with using renum, find a bug, or have a feature request, feel free to [file an issue](https://github.com/Zephyrkul/sans/issues/new/choose).

## Examples

Parsing from standard input:

```py
import regex
from renum import renum


class Actions(renum, flags=regex.IGNORECASE):
    GO = r"go (?P<direction>north|south|east|west)"
    EXAMINE = r"examine (?P<item>[\w\s]+)"
    OPEN = r"open (?P<object>door|chest)"


if __name__ == "__main__":
    while True:
        line = input()
        if not line:
            break
        action = Actions.match(line)  # The renum class acts like a Pattern...
        if action is Actions.GO:
            print("You went %s" % action.group("direction"))  # and each entry acts like a Match
        elif action is Actions.EXAMINE:
            print("You take a closer look at %s. Looks grungy." % action.group("item"))
        elif action is Actions.OPEN:
            print("You tried to open the %s, but it was locked." % action.group("object"))
        else:
            print("Unknown action: %s" % line)
```

Troubleshooting a misbehaving renum:

```pycon
>>> import regex
>>> from renum import renum
>>>
>>> class Bad(renum, flags=regex.IGNORECASE | regex.DEBUG):
...     GOOD = r"no (?:issues|problems) here"
...     BAD = r"whoops,\s(?P<missed something)"
...
regex.error: bad character in group name at position 29 in BAD
whoops,\s(?P<missed something)
                             ^
```

## Requirements

- [Python 3.9+](https://www.python.org/)
- [regex](https://pypi.org/project/regex/)

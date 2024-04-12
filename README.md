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

Scanning through happenings from an XML file:

```py
import xml.etree.ElementTree as ET

from renum import renum


class HappeningsRenum(renum):
    ADMITTED = r"@@(?P<nation>[^@]+)@@ was admitted to the World Assembly\."
    MOVED = r"@@(?P<nation>[^@]+)@@ relocated from %%(?P<from>[^%]+)%% to %%(?P<to>[^%]+)%%\."
    ENDORSED = r"@@(?P<endorser>[^@]+)@@ endorsed @@(?P<endorsee>[^@]+)@@\."
    WITHDREW_ENDORSEMENT = r"@@(?P<endorser>[^@]+)@@ withdrew its endorsement from @@(?P<endorsee>[^@]+)@@\."


def main():
    root = ET.parse("happenings.xml")
    for element in root.iterfind("HAPPENINGS/EVENT/TEXT"):
        event = HappeningsRenum.fullmatch(element.text)
        if event is HappeningsRenum.ADMITTED:
            print("Welcome to the WA, %s!" % event.last_match.group("nation"))
        elif (
            event is HappeningsRenum.MOVED
            and event.last_match.group("to") == "the_rejected_realms"
        ):
            print("Welcome to TRR, %s!" % event.last_match.group("nation"))
        elif (
            event is HappeningsRenum.ENDORSED
            and event.last_match.group("endorsee") == "zephyrkul"
        ):
            print(
                "Thanks for the endorsement, %s!" % event.last_match.group("endorser")
            )
        elif (
            event is HappeningsRenum.WITHDREW_ENDORSEMENT
            and event.last_match.group("endorsee") == "zephyrkul"
        ):
            print("But why, %s? \N{PENSIVE FACE}" % event.last_match.group("endorser"))


if __name__ == "__main__":
    main()
```

## Requirements

- [Python 3.7+](https://www.python.org/)
- [regex](https://pypi.org/project/regex/)

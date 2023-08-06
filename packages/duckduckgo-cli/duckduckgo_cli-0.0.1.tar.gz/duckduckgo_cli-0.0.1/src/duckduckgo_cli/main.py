"""
---
WORK IN PROGRESS
---

# duckduckgo-cli
Search duckduckgo in terminal open browser

## Install
```
pip install duckduckgo-cli
```

## Typical usage examples
```
$ ddg !py3 webbrowser # searches "!py3 webbrowser" on https://duckduckgo.com/
```
"""
__version__ = "0.0.1"

from html import escape
from sys import argv
from webbrowser import open


def convert_argv_to_duckduckgo_link(arr: list[str]) -> str:
    return f"https://duckduckgo.com/?q={escape('+'.join(arr))}"


def open_duckduckgo_link_in_browser(link: str) -> None:
    open(link)


def main() -> None:
    open_duckduckgo_link_in_browser(convert_argv_to_duckduckgo_link(argv))

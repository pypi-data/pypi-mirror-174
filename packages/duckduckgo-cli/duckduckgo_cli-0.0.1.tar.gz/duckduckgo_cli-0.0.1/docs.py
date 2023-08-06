# type: ignore

from sys import path

import tomli
import tomli_w

path.insert(0, "./src/duckduckgo_cli")

import main

with open("README.md", "w") as f:
    f.write(main.__doc__)

with open("pyproject.toml", "rb") as f:
    toml = tomli.load(f)

print(
    f'updating `pyprojet.toml` version from `{toml["project"]["version"]}` to `{main.__version__}`'
)
toml["project"]["version"] = main.__version__

with open("pyproject.toml", "w") as f:
    f.write(tomli_w.dumps(toml))

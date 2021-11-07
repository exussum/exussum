import toml
import os
from collections import namedtuple as nt
import shutil


class Opt:
    findfile = """
Usage:
  findfile <file>...
"""

    findcode = """
Usage:
  findcode <rg-params>... <pattern>
"""

    findfilecode = """
Usage:
  findfilecode glob [<rg-params>...] <pattern>
"""


def setup(override_included_files=()):
    Config = nt("Config", "unix src")
    Src = nt("Src", "root included_files excluded_files excluded_paths")
    Unix = nt("Unix", "rg")
    home = os.path.expanduser("~")

    try:
        with open(f"{home}/.exussum.ini") as fh:
            raw = toml.load(fh)
            if override_included_files:
                raw["src"]["included_files"] = override_included_files
            return Config(Unix(**raw["unix"]), Src(**raw["src"]))
    except FileNotFoundError:
        print("~/.exussum.ini not found")
        cfg = {
            "unix": {"rg": shutil.which("rg")},
            "src": {
                "root": input("Entre root directory: "),
                "included_files": input( "Entre included file globs separated by spaces: ").split(),
                "excluded_files": input( "Entre excluded file globs separated by spaces: ").split(),
                "excluded_paths": input( "Entre excluded paths separated by spaces: ").split(),
            },
        }
        with open(f"{home}/.exussum.ini", "w") as fh:
            toml.dump(cfg, fh)
        return setup(override_included_files)


def err(msg):
    print(msg)
    exit(1)

import toml
import os
from collections import namedtuple as nt


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

    with open(f"{home}/.exussum.ini") as fh:
        raw = toml.load(fh)
        if override_included_files:
            raw["src"]["included_files"] = override_included_files
        result = Config(Unix(**raw["unix"]), Src(**raw["src"]))
        return result


def err(msg):
    print(msg)
    exit(1)

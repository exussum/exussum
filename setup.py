#!/usr/bin/env python

from distutils.core import setup

setup(
    name="exussum",
    version="1.0",
    install_requires=["toml == 0.10.2"],
    scripts=[
        "exussum/bin/findcode",
        "exussum/bin/findfile",
        "exussum/bin/findfilecode",
    ],
    packages=["exussum"],
)

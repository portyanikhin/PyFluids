#  PyFluids
#  Copyright (c) 2021 Vladimir Portyanikhin

import os

from setuptools import setup, find_packages

AUTHOR = "Vladimir Portyanikhin"
AUTHOR_EMAIL = "v.portyanikhin@ya.ru"
DESCRIPTION = "A simple, full-featured, lightweight CoolProp wrapper for Python"
KEYWORDS = [
    "CoolProp",
    "fluids",
    "mixtures",
    "humid",
    "air",
    "thermophysical",
    "properties",
]
NAME = "pyfluids"
VERSION = "1.0.2"
PYTHON_REQUIRES = ">=3.7, <3.9"
URL = "https://github.com/portyanikhin/PyFluids"
LICENSE = "MIT"
CLASSIFIERS = [
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: Implementation :: PyPy",
]
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "requirements.txt")) as file:
    INSTALL_REQUIRES = [
        i for i in file.read().splitlines() if not i.startswith("pytest")
    ]
with open(os.path.join(here, "README.md")) as file:
    LONG_DESCRIPTION = file.read()

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    keywords=KEYWORDS,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    packages=find_packages(exclude=["tests"]),
    install_requires=INSTALL_REQUIRES,
    python_requires=PYTHON_REQUIRES,
    url=URL,
    license=LICENSE,
    classifiers=CLASSIFIERS,
)

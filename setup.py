import os

from setuptools import setup, find_packages

NAME = "pyfluids"
VERSION = "2.2.1"
DESCRIPTION = "A simple, full-featured, lightweight CoolProp wrapper for Python"
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "PyPI.md")) as file:
    LONG_DESCRIPTION = file.read()
LONG_DESCRIPTION_CONTENT_TYPE = "text/markdown"
AUTHOR = "Vladimir Portyanikhin"
AUTHOR_EMAIL = "v.portyanikhin@ya.ru"
URL = "https://github.com/portyanikhin/PyFluids"
DOWNLOAD_URL = "https://pypi.org/project/pyfluids"
EXCLUDE = ["tests"]
CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Intended Audience :: Education",
    "Intended Audience :: Manufacturing",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: MacOS",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: POSIX :: Linux",
    "Operating System :: Unix",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: Implementation",
    "Programming Language :: Python :: Implementation :: PyPy",
    "Topic :: Education",
    "Topic :: Scientific/Engineering",
    "Topic :: Scientific/Engineering :: Atmospheric Science",
    "Topic :: Scientific/Engineering :: Chemistry",
    "Topic :: Scientific/Engineering :: Physics",
]
LICENSE = "MIT"
KEYWORDS = [
    "CoolProp",
    "fluids",
    "mixtures",
    "humid",
    "air",
    "thermophysical",
    "properties",
    "thermodynamics",
]
PLATFORMS = ["MacOS", "Windows", "Linux", "Unix"]
with open(os.path.join(here, "requirements.txt")) as file:
    INSTALL_REQUIRES = [
        i for i in file.read().splitlines() if not i.startswith("pytest")
    ]
PYTHON_REQUIRES = ">=3.7, <3.11"


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    download_url=DOWNLOAD_URL,
    packages=find_packages(exclude=EXCLUDE),
    classifiers=CLASSIFIERS,
    license=LICENSE,
    keywords=KEYWORDS,
    platforms=PLATFORMS,
    install_requires=INSTALL_REQUIRES,
    python_requires=PYTHON_REQUIRES,
)

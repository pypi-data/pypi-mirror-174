#!/usr/bin/env python
import sys
import pathlib
import tomllib
from setuptools import find_packages, setup

WORK_DIR = pathlib.Path(__file__).parent

# Check python version
MINIMAL_PY_VERSION = (3, 10, 8)
if sys.version_info < MINIMAL_PY_VERSION:
    raise RuntimeError("aiogram works only with Python {}+".format(".".join(map(str, MINIMAL_PY_VERSION))))


def get_description() -> str:
    """
    Read full description from "README.rst"
    :return: description
    :rtype: str
    """
    with open("README.md", "r", encoding="utf-8") as f:
        return f.read()


def get_meta_info() -> dict:
    try:
        with open("pyproject.toml", "rb") as f:
            return tomllib.load(f)
    except IndexError:
        raise RuntimeError('Unable to determine version.')


project_meta = get_meta_info()
project_dir = project_meta["project"]["name"].replace("-", "_")

setup(
    license="MIT",
    name=project_meta["project"]["name"],
    version=project_meta["project"]["version"],
    author=project_meta["project"]["authors"][0]["name"],
    author_email=project_meta["project"]["authors"][0]["email"],
    description=project_meta["project"]["description"],
    long_description=get_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/frontdevops/apiogram",
    download_url=("https://github.com/frontdevops/apiogram/archive/refs/tags/"
                  f'{project_meta["project"]["version"]}.tar.gz'),
    project_urls={
        "Documentation": "https://github.com/frontdevops/apiogram/blob/main/README.md",
        "Source": "https://github.com/frontdevops/apiogram",
        "Bug Tracker": "https://github.com/frontdevops/apiogram/issues",
    },
    keywords=["aiogram", "telegram", "storage"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10.8",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Application Utilities",
    ],
    package_dir={"": project_dir},
    packages=find_packages(where=project_dir,
                           exclude=("tests", "tests.*", "examples.*", "docs",),
                           ),
    include_package_data=False,
    python_requires=">=3.10.8",
    install_requires=[
        "aiogram>=2.22.2",
        "magic-config>=0.1.10",
        "geekjob-python-helpers>=1.0.0",
        "nosql-storage-wrapper>=0.1.0"
    ],
    extras_require={
        "dev": [
            "pytest >= 3.7",
            "check-manifest",
            "twine"
        ]
    },
)

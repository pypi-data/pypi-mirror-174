from io import open
from setuptools import setup


version = "0.0.1"

setup(
    name="pip_command",
    version=version,

    author="pavelgs",
    author_email="p6282813@yandex.ru",

    description="lib for fast work with pip commands",
    long_description="README.md",

    url="https://github.com/pavelglazunov/pip-command",

    license="Apache License, Version 2.0, see LICENSE file",

    packages=["pip_command"]
)
from io import open
from setuptools import setup


version = "0.0.3"

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pip_command",
    version=version,

    author="pavelgs",
    author_email="p6282813@yandex.ru",

    description="lib for fast work with pip commands",
    long_description=long_description,
    long_description_content_type="text/markdown",

    url="https://github.com/pavelglazunov/pip-command",

    license="Apache License, Version 2.0, see LICENSE file",

    packages=["pip_command"]
)
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="opentsp",
    version="1.1.3",
    description="Generate TSP instances and test hypotheses on them",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/james-langbein/OpenTSP",
    author="James Langbein",
    author_email="james.langbein@protonmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Development Status :: 4 - Beta",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=['matplotlib', 'numpy'],
)

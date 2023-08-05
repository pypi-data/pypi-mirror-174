#!/usr/bin/env python

import os
from setuptools import setup

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

version = os.environ.get("BUILD_VERSION")

if version is None:
    with open("VERSION", "r") as version_file:
        version = version_file.read().strip()

setup(
    name="sphinxter",
    version=version,
    package_dir = {'': 'lib'},
    py_modules = [
        'sphinxter',
        'sphinxter.reader',
        'sphinxter.document',
        'sphinxter.writer'
    ],
    install_requires=[
        'Sphinx==5.1.1',
        'PyYAML==6.0'
    ],
    url=f"https://sphinxter.readthedocs.io/en/{version}/",
    download_url="https://github.com/gaf3/sphinxter",
    author="Gaffer Fitch",
    author_email="sphinxter@gaf3.com",
    description="Autodoc converting YAML docstrings and code comments to sphinx documentation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license_files=('LICENSE.txt',),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ]
)

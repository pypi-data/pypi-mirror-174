#!/usr/bin/env python

import sys
from os import path

from setuptools import find_packages, setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


install_requires = [
    "orjson>=3"
]

# Require python 3.8
if sys.version_info.major != 3 and sys.version_info.minor < 8:
    sys.exit("'easy_signer' requires Python >= 3.8")

setup(
    name="easy_signer",
    version="0.1.0",
    author="Paaksing",
    author_email="paaksingtech@gmail.com",
    url="https://github.com/paaksing/easy_signer",
    description="Simple package for cryptographic signing",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=["signing", "cryptographic", "security"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.8",
        "Environment :: Web Environment",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Natural Language :: English",
    ],
    license="MIT",
    zip_safe=True,
    packages=find_packages(exclude=("tests", "benchmark")),
    install_requires=install_requires,
    include_package_data=True,
)

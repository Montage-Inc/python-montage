#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

setup(
    name='montage',
    version='2.0.0',
    author='Derek Payton',
    author_email='dpayton@mntge.com',
    description='Python bindings for Montage',
    long_description=open('./README.rst', 'r').read(),
    keywords='data',
    license='MIT',
    url='https://github.com/EditLLC/python-montage',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'cached_property==1.3.0',
        'jsonschema==2.5.1',
        'requests==2.9.1',
    ],
)

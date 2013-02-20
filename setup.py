#!/usr/bin/env python

import os
from setuptools import setup

setup(
    name='wthr',
    version='0.1',
    url='https://github.com/lavelle/wthr.py',

    author='Giles Lavelle',
    author_email='giles.lavelle@gmail.com',

    description='Check the weather from the command line',
    long_description=open(os.path.join(os.path.dirname(__file__), 'readme.md')).read(),

    install_requires=[

    ],
    py_modules=[
        'wthr',
    ],
    entry_points={
        'console_scripts': ['wthr=wthr:main']
    }
)

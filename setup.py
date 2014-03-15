#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='pyspec',
    version='0.0.1',
    description='Behavior-driven development description language',
    author='Zac Stewart',
    url='https://github.com/zacstewart/pyspec',
    packages=find_packages('.', exclude=['tests']),
    entry_points={
        'console_scripts': ['pyspec = pyspec.runner:main']
        }
    )

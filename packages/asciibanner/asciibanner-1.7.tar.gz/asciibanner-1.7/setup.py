#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Python Version    : 3.X
# Author            : Dicahsin
# File name         : setup.py

from setuptools import setup

with open("DESCRIPTION.txt") as file:
    description = file.read()

with open("README.md") as file:
    long_description = file.read()

REQUIREMENTS = ['numpy', 'Pillow']

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3',
    'Environment :: Console',
    'Natural Language :: English'
    ]

setup(name='asciibanner',
    version='1.7',
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://root-me.org',
    author='Dicashsin',
    author_email='dicahsin@proton.me',
    license='MIT',
    packages=['asciibanner'],
    classifiers=CLASSIFIERS,
    install_requires=REQUIREMENTS
    )

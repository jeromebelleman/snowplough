#!/usr/bin/env python
# coding=utf-8

import os
from distutils.core import setup

delattr(os, 'link')

setup(
    name='snowplough',
    version='1.0',
    author='Jerome Belleman',
    author_email='Jerome.Belleman@gmail.com',
    url='http://cern.ch/jbl',
    description="Shovel off ServiceNow tickets",
    long_description="Snowplough is a simple-minded tool which creates indices and body-searches vast quantities of ServiceNow tickets.",
    scripts=['snowplough'],
    data_files=[('/usr/share/man/man1', ['snowplough.1'])],
)

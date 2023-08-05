#!/usr/bin/env python

from __future__ import print_function

import sys

from setuptools import setup

if sys.version_info < (2, 7):
    print("Python versions prior to 2.7 are not supported for pip installed mlsql-plugin.",
          file=sys.stderr)
    sys.exit(-1)

try:
    exec(open('version.py').read())
except IOError:
    print("Failed to load mlsql-plugin version file for packaging.",
          file=sys.stderr)
    sys.exit(-1)

VERSION = __version__

setup(
    name='byzer_cocodataset',
    version=VERSION,
    description='Byzer tool to generate cocodata meta file',
    long_description="Byzer tool to generate cocodata meta file",
    author='WilliamZhu',
    author_email='allwefantasy@gmail.com',
    url='https://github.com/allwefantasy/byzer-cocodataset',
    packages=['tech',
              'tech.mlsql',
              'tech.mlsql.plugin',
              'tech.mlsql.plugin.ds.coco',
              ],
    include_package_data=True,
    license='http://www.apache.org/licenses/LICENSE-2.0',
    install_requires=[
        'numpy',
        'pandas',
        'pypandoc',
        'Pillow'
    ],
    setup_requires=['pypandoc'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy']
)

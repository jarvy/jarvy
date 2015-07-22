#!/usr/bin/env python

import os
import re
import sys

from codecs import open

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

packages = [
    'jarvy',
    'jarvy.packages',
    'jarvy.packages.google',
]

requires = ['beautifulsoup4', 'google']

version = ''
with open('jarvy/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()
with open('HISTORY.rst', 'r', 'utf-8') as f:
    history = f.read()

setup(
    name='jarvy',
    version=version,
    description='Python Intelligent Assistant for Humans.',
    long_description=readme + '\n\n' + history,
    author='Semih Yagcioglu',
    author_email='semihyagcioglu@yahoo.com',
    url='http://github.com/jarvy/jarvy',
    packages=packages,
    package_data={'': ['LICENSE']},
    package_dir={'jarvis': 'jarvis'},
    include_package_data=True,
    install_requires=requires,
    license='MIT',
    zip_safe=False,
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
    ),
)

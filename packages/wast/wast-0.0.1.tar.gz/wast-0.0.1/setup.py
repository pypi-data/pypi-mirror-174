#!/usr/bin/env python3
import os
from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name = 'wast',
    version = '0.0.1',
    description = 'Wolphin AST',
    long_description = readme,
    long_description_content_type='text/markdown',
    author = 'Wolphin',
    author_email = 'q@wolph.in',
    url = 'https://gitlab.com/qwolphin/wast',
    packages = find_packages(),
    #package_data={'kdsl': ['py.typed']},
    #zip_safe=False,
    #install_requires=[
    #    'attrs',
    #    'pyyaml',
    #    'envparse',
    #    'python-dotenv',
    #],
    classifiers = [
        'Typing :: Typed',
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)

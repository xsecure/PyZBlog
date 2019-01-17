#!/usr/bin/env python

from setuptools import setup, find_packages

_VERSION = '0.0.1'

setup(
    name = 'PyZBlog',
    version = _VERSION,
    url = 'https://github.com/xsecure/PyZBlog/',
    project_urls = {},
    description = 'A python libary for Z-Blog',
    packages = find_packages(exclude=[]),
    install_requires = [
        'pymysql>=0.9.3'
    ],
)

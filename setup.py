# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", 'r') as readme:
    long_desc = readme.read()

setup(
    name='mlhearts',
    version='0.1',
    url='https://github.com/mneyrane/mlhearts',
    license='MIT',
    python_requires='>=3.7',
    test_suite='mlhearts.tests',
    packages=find_packages(exclude=['tests']),
    include_package_data=True
)
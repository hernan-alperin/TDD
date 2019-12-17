# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='segmemtador en TDD',
    version='0.1.0',
    description='Test Designed Dev del segmantador para el censo202',
    long_description=readme,
    author='Hernán Alperin',
    author_email='alpe@alum.mit.edu',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)


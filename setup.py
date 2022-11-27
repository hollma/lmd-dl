# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='lmd-dl',
    version='0.1.0',
    description='',
    long_description=readme,
    author='hollma',
    author_email='hollma@mailbox.org',
    url='https://github.com/hollma/lmd-dl/',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
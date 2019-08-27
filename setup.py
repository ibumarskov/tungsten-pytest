#!/usr/bin/env python

import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def get_requirements_list(requirements):
    all_requirements = read(requirements)
    return all_requirements


setup(
    name='tungsten_tests',
    version=0.1,
    description='Component tests for TungstenFabric with OpenStack on '
                'KaaS platform',
    url='https://www.mirantis.com/',
    author='Mirantis',
    packages=find_packages(),
    include_package_data=True,
    install_requires=get_requirements_list('./requirements.txt'),
)

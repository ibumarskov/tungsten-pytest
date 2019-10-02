# Gerrit-CI [![BuildStatus](https://travis-ci.com/ibumarskov/tungsten-pytest.svg?branch=master)](https://travis-ci.com/ibumarskov/tungsten-pytest)

# Tungsten-pytest
Tunsgten Fabric tests for MCP KaaS.

## Overview
The tungsten-pytest repository contains the pytest-based tests for validating integration of Tungsten Fabric with OpenStack within Mirantis KaaS environment. Tests can be run directly or using appropriate docker image.

## Limitations
Python 2.7 is only supported (due to contrail-api-client limitations).

## Configuration
Tungsten-pytest uses following configuration files:
* *tungsten-pytest.cfg* - contains main settings for access to tungsten/openstack api and some data about k8s environment
* *kubeconfig* - kube config file are used to access to k8s environment
Examples of configuration files can be found in *etc/* directory

## Running tests
There are two way to running tests: directly from repository and using docker image

### Run tests from repository
To run tunsgten-pytest against your KaaS environment with Openstack+TungstenFabric:
1. Install and activate virtual environment with python 2.7
`virtualenv .venv
source .venv/bin/activate`
2. Install required packages
`pip install -r requirements.txt`
3. Create configuration file with parameters and put it to *etc/tungsten-pytest.cfg*
Or you can set another place using TFT_CONF env variable.
4. Copy kube config file to *etc/kubeconfig*
Or you can set another place using TFT_KUBECONFIG env variable.
5. Run smoke tests and save results to xml (just for example):
`pytest  --junit-xml=data/results.xml -m smoke`

### Run tests from docker image
\#TO DO


## How to build docker image
Before build docker image from local copy of repository remove all `.*pyc` files and `__pycache__` folder:

`find tungsten_tests/ -name "*.pyc" -exec rm -f {} \;
rm -rf tungsten_tests/tests/__pycache__`

> Make sure you don't have any sensitive data in etc/ and data/ folders
Then build image as usually:
`docker build --tag=tungsten-pytest .`

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
```
virtualenv .venv
source .venv/bin/activate
```
2. Install required packages
`pip install -r requirements.txt`
3. Create configuration file with parameters and put it to *etc/tungsten-pytest.cfg*
Or you can set another place using TFT_CONF env variable.
4. Copy kube config file to *etc/kubeconfig*
Or you can set another place using TFT_KUBECONFIG env variable.
5. Run smoke tests and save results to xml:
`pytest --junit-xml=data/results.xml -m smoke`

### Run tests from docker image
To run tunsgten-pytest against your KaaS environment with Openstack+TungstenFabric using docker image:
1. Pull docker image from [dockerhub](https://hub.docker.com/r/bumarskov/tungsten-pytest)
`docker push bumarskov/tungsten-pytest:<tagname>`
2. Create directory with following structure:
```
    user@user-pc:~/tft$ tree
    .
    ├── data
    │   ├── images
    │   └── keys
    └── etc
```
3. Create configuration file with parameters and put it to *etc/tungsten-pytest.cfg*
4. Copy kube config file to *etc/kubeconfig*
5. Run smoke tests using docker with mounted *etc* and *data* folders:
`docker run -v '<path_to_data_dir>:/tungsten-pytest/data' -v '<path_to_etc_dir>:/tungsten-pytest/etc' -e PYTEST_ARGS='-m smoke' --network=host tungsten-pytest`


## How to build docker image
Before build docker image from local copy of repository remove all `.*pyc` files and `__pycache__` folder:

`find tungsten_tests/ -name "*.pyc" -exec rm -f {} \;
rm -rf tungsten_tests/tests/__pycache__`

> Make sure you don't have any sensitive data in etc/ and data/ folders
Then build image as usually:
`docker build --tag=tungsten-pytest .`

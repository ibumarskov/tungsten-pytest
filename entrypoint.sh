#!/bin/bash

set -xe

function _info(){
  set +x
  echo -e "============================= INFO: List of tests ============================="
  pytest --collect-only
  set -x
}

_info

if [ -z "$RES_PATH" ]; then
  RES_PATH=data/results.xml
fi

pytest --junit-xml=$RES_PATH $PYTEST_ARGS

#!/bin/bash

VIRTUAL_ENV_NAME='env'

python3 -m venv $VIRTUAL_ENV_NAME && source ./$VIRTUAL_ENV_NAME/bin/activate
python3 -m pip install -U pip wheel setuptools

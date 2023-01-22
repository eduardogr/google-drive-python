#!/bin/bash

#
# Code based in: https://github.com/opentensor/bittensor/blob/master/scripts/release/release_pip.sh
#

####
# Utils
####
source ${BASH_SOURCE%/*}/utils.sh
###

# 1. Cleaning up
echo_info "Removing dirs: dist/ and build/"
rm -rf dist/
rm -rf build/

# 2. Creating python wheel
echo_info "Generating python wheel"
python3 setup.py sdist bdist_wheel

# 3. Upload wheel to pypi
echo_info "Uploading python wheel"
python3 -m twine upload dist/*

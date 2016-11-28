#!/bin/bash
$PYTHON35 -m venv .
source bin/activate
pip install -U setuptools zc.buildout
./bin/buildout -c experimental/py3x-test.cfg
./bin/test --xml

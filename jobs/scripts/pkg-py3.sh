#!/bin/bash
pip install -U setuptools zc.buildout
./bin/buildout -c experimental/py3x-test.cfg
./bin/test --xml

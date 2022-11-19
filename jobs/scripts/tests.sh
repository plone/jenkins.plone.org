#!/bin/sh

PYTHON_VERSION="{py}"
/srv/python${{PYTHON_VERSION}}/bin/python3 -m venv venv
. venv/bin/activate

pip install -r requirements.txt

buildout buildout:git-clone-depth=1 -c buildout.cfg
bin/test --xml

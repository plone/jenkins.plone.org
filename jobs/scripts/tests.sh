#!/bin/bash
set -x

PYTHON_VERSION="{py}"
PLONE_VERSION="{plone-version}"
/srv/python${{PYTHON_VERSION}}/bin/python3 -m venv venv
. venv/bin/activate

pip install -r requirements.txt

buildout buildout:git-clone-depth=1 -c buildout.cfg

if [[ "${{PLONE_VERSION}}" == 6* ]]; then
  bin/test --xml .
else
  bin/test --xml
fi

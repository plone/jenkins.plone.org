#!/bin/sh
pip install -r requirements.txt

BUILDOUT="buildout.cfg"
SCRIPT="bin/test"

buildout buildout:git-clone-depth=1 -c ${BUILDOUT}
${SCRIPT} --xml

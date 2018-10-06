#!/bin/sh
pip install -Ur requirements.txt
buildout buildout:git-clone-depth=1
bin/alltests-at --all --xml

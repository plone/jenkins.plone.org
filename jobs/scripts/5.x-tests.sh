#!/bin/bash
pip install -r requirements.txt
buildout buildout:git-clone-depth=1 -c core.cfg
bin/alltests --xml

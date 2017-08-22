#!/bin/bash
sed -i 's/    mr.developer/    mr.developer\ngit-clone-depth = 100/' core.cfg
pip install -r requirements.txt
buildout -c jenkins.cfg
bin/alltests-at --xml

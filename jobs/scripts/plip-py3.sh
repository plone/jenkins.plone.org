#!/bin/bash
sed -i 's/    mr.developer/    mr.developer\ngit-clone-depth = 100/' core.cfg
pip install -r requirements.txt
buildout -c py3.cfg

./bin/test -s plone.app.contenttypes
#!/bin/bash
sed -i 's/    mr.developer/    mr.developer\ngit-clone-depth = 100/' core.cfg
pip install -r requirements.txt
buildout -c jenkins.cfg
#bin/pybot -v BROWSER:phantomjs src/Products.CMFPlone/Products/CMFPlone/tests/robot/robodoc
bin/pybot src/Products.CMFPlone/Products/CMFPlone/tests/robot/robodoc

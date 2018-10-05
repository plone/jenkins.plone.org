#!/bin/bash
pip install -r requirements.txt
buildout buildout:git-clone-depth=1 -c core.cfg
ROBOT_BROWSER={browser}
ROBOTSUITE_PREFIX=ONLYROBOT
bin/alltests -t ONLYROBOT --all --xml

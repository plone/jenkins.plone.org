#!/bin/bash
# run buildout and tests
{pybinary} bootstrap.py -c jenkins.cfg
bin/buildout buildout:git-clone-depth=1 -c jenkins.cfg

export PATH="/usr/lib/chromium-browser:$PATH"
export ROBOT_BROWSER=chrome

xvfb-run -a --server-args='-screen 0 1920x1200x24' bin/jenkins-alltests -1

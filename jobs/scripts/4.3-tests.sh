#!/bin/sh
# run buildout and tests
{pybinary} bootstrap.py -c jenkins.cfg
bin/buildout buildout:git-clone-depth=1 -c jenkins.cfg

export PATH="/usr/lib/chromium-browser:$PATH"
export ROBOT_BROWSER=headlesschrome

bin/jenkins-alltests -1

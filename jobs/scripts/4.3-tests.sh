#!/bin/bash
# run buildout and tests
{pybinary} bootstrap.py -c jenkins.cfg
bin/buildout -c jenkins.cfg

ROBOT_BROWSER=chrome
bin/jenkins-alltests -1

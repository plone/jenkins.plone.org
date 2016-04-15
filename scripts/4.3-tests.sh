#!/bin/bash
# run buildout and tests
{pybinary} bootstrap.py -c jenkins.cfg
./marker.sh set $$
bin/buildout -c jenkins.cfg
./marker.sh release
bin/jenkins-alltests -1

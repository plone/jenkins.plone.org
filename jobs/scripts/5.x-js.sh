#!/bin/sh
# run mockup tests
echo $PATH
node --version
npm --version
make bootstrap
make test-jenkins

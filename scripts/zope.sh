#!/usr/bin/env bash
cat > jenkins.cfg << EOF
[buildout]
extends = buildout.cfg
parts +=
    jenkins-test

[jenkins-test]
recipe = collective.xmltestreport
eggs =
    \${{alltests:eggs}}

[versions]
collective.xmltestreport = 1.3.3
EOF
{pybinary} bootstrap.py -c jenkins.cfg
bin/buildout -c jenkins.cfg
bin/jenkins-test --xml

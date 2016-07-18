#!/usr/bin/env bash
{pybinary} bootstrap.py -c experimental/cmf.cfg
bin/buildout -c experimental/cmf.cfg
bin/jenkins-test --xml

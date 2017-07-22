#!/usr/bin/env bash
{pybinary} bootstrap.py -c development-python2.cfg
bin/buildout -t 3 -v -c development-python2.cfg
rm src/zope.component/src/zope/component/tests/test_standalone.py
bin/test-ztk

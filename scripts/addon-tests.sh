#!/bin/bash
if [ "{plone-version}" = "4.3" ]; then
    $PYTHON27 bootstrap.py -c jenkins.cfg
else
    $PYTHON27 bootstrap.py --setuptools-version 31.1.1 --buildout-version 2.8.0 -c jenkins.cfg
fi

bin/buildout -c jenkins.cfg
bin/test --xml -s ${{ADDON_NAME}}

if [ "${{REPORT_ON_GITHUB}}" = "True" ]; then
    $PYTHON27 templates/addon-report-status.py
fi

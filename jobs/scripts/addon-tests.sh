#!/bin/bash
if [ "{plone-version}" = "4.3" ]; then
    python bootstrap.py -c jenkins.cfg
    bin/buildout -c jenkins.cfg
else
    python bootstrap.py --setuptools-version 33.1.1 --buildout-version 2.8.0 -c core.cfg
    bin/buildout -c core.cfg
fi

bin/test --xml -s ${{ADDON_NAME}}

if [ "${{REPORT_ON_GITHUB}}" = "True" ]; then
    python templates/addon-report-status.py
fi

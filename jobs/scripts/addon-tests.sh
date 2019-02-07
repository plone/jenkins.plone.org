#!/bin/sh
if [ "{plone-version}" = "4.3" ]; then
    python bootstrap.py -c jenkins.cfg
    bin/buildout buildout:git-clone-depth=1 -c jenkins.cfg
else
    if [ "{plone-version}" = "5.2" ]; then
        pip install -r requirements.txt
        buildout buildout:git-clone-depth=1 -c core.cfg
    else
        python bootstrap.py --setuptools-version 33.1.1 --buildout-version 2.8.0 -c core.cfg
        bin/buildout buildout:git-clone-depth=1 -c core.cfg
    fi
fi

bin/test --xml -s ${{ADDON_NAME}}

if [ "${{REPORT_ON_GITHUB}}" = "True" ]; then
    python templates/addon-report-status.py
fi

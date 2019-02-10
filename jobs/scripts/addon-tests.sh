#!/bin/sh
OPTIONS="buildout:git-clone-depth=1 buildout:allow-picked-versions=true buildout:show-picked-versions=true"
if [ "{plone-version}" = "4.3" ]; then
    python bootstrap.py -c jenkins.cfg
    bin/buildout $OPTIONS -c jenkins.cfg
else
    pip install -r requirements.txt
    buildout $OPTIONS -c core.cfg
fi

bin/test --xml -s ${{ADDON_NAME}}

if [ "${{REPORT_ON_GITHUB}}" = "True" ]; then
    python templates/addon-report-status.py
fi

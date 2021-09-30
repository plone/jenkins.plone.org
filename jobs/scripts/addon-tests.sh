#!/bin/sh
OPTIONS="buildout:git-clone-depth=1 buildout:allow-picked-versions=true buildout:show-picked-versions=true"
pip install -r requirements.txt
buildout $OPTIONS -c core.cfg

bin/test --xml -s ${{ADDON_NAME}}

if [ "${{REPORT_ON_GITHUB}}" = "True" ]; then
    python templates/addon-report-status.py
fi

#!/bin/sh
OPTIONS="buildout:git-clone-depth=1 buildout:show-picked-versions=True"

pip install -r requirements.txt
buildout $OPTIONS -c core.cfg

bin/test --xml -s ${{ADDON_NAME}}

if [ "${{REPORT_ON_GITHUB}}" = "True" ]; then
    python templates/addon-report-status.py
fi

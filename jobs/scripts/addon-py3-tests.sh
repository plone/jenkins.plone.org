#!/bin/sh
pip install -r requirements.txt
buildout buildout:git-clone-depth=1 -c core.cfg

bin/test --xml -s ${{ADDON_NAME}}

if [ "${{REPORT_ON_GITHUB}}" = "True" ]; then
    python templates/addon-report-status.py
fi

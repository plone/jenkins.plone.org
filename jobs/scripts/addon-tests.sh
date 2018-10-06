#!/bin/sh
python bootstrap.py
bin/buildout buildout:git-clone-depth=1

bin/test --all --xml -s ${{ADDON_NAME}}

return_code="$?"

if [ "${{REPORT_ON_GITHUB}}" = "True" ]; then
    python templates/addon-report-status.py
fi

exit "$return_code"

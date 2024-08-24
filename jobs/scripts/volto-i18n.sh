#!/bin/bash
set -x

VOLTO_BRANCH="{branch}"

python -m venv venv
. venv/bin/activate
pip install i18ndude

export PYTHONIOENCODING=utf-8

if [ "${{VOLTO_BRANCH}}" = "main" ]; then
  path="packages/volto/locales"
  parent_path="../../.."
else
  path="locales"
  parent_path=".."
fi

cd ${{path}}
i18ndude list -p volto > ${{parent_path}}/volto-i18n-report.txt

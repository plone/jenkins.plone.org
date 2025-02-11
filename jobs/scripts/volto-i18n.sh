#!/bin/bash
set -x

VOLTO_BRANCH="{branch}"

export PYTHONIOENCODING=utf-8

if [ "${{VOLTO_BRANCH}}" = "main" ]; then
  path="packages/volto/locales"
  parent_path="../../.."
else
  path="locales"
  parent_path=".."
fi

cd ${{path}}
uv run -p {py} --with i18ndude i18ndude list -p volto > ${{parent_path}}/volto-i18n-report.txt

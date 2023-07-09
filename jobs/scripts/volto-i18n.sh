#!/bin/bash
set -x

python -m venv venv
. venv/bin/activate
pip install i18ndude

export PYTHONIOENCODING=utf-8

cd locales
i18ndude list -p volto > ../volto-18n-report.txt

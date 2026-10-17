#!/bin/sh
set -x

uv run -p {py} --with-requirements requirements.txt buildout buildout:git-clone-depth=1 -c experimental/i18n.cfg install i18n-find-untranslated i18ndude

export PYTHONIOENCODING=utf-8
bin/i18n-find-untranslated details > missing.txt || echo 0

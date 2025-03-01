#!/bin/bash
set -x

uv run -p {py} --with-requirements requirements.txt buildout buildout:git-clone-depth=1 -c buildout.cfg

bin/test --xml .

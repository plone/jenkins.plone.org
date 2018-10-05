#!/usr/bin/env bash
pip install -r requirements.txt
buildout buildout:git-clone-depth=1 -c buildout.cfg
bin/sphinx-build source build

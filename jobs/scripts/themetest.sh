#!/usr/bin/env bash
pip install -r requirements.txt
buildout buildout:git-clone-depth=1 -c buildout.cfg
xvfb-run -a --server-args='-screen 0 1920x1200x24' bin/sphinx-build source build

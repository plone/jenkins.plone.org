#!/usr/bin/env bash
pip install -r requirements.txt
buildout -c buildout.cfg
bin/sphinx-build source build

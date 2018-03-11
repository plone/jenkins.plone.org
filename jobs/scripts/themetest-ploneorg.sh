#!/usr/bin/env bash
pip install zc.buildout==2.11.0 setuptools==38.4.0
buildout -c buildout.cfg
bin/sphinx-build src/plone.themepreview/source build

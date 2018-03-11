#!/usr/bin/env bash
sed -i 's/    mr.developer/    mr.developer\ngit-clone-depth = 100/' core.cfg
pip install -r requirements.txt
buildout -c core.cfg
grep -RI ZopeTestCase parts/packages > deps.txt.tmp || echo 0
sed -i 's|parts/packages||' deps.txt.tmp
grep -Ev '/(Testing|OFS|PloneTestCase|Zope2|ZPublisher)/' deps.txt.tmp > deps.txt

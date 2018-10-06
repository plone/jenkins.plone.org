#!/usr/bin/env bash
pip install -Ur requirements.txt
buildout buildout:git-clone-depth=1
grep -RI ZopeTestCase parts/packages > deps.txt.tmp || echo 0
sed -i 's|parts/packages||' deps.txt.tmp
grep -Ev '/(Testing|OFS|PloneTestCase|Zope2|ZPublisher)/' deps.txt.tmp > deps.txt

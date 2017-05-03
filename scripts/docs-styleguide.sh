#!/usr/bin/env bash
cat > docs.cfg << EOF
[buildout]
extends = core.cfg
auto-checkout = *
git-clone-depth = 100
EOF
sed -i 's/^Zope2/#Zope2/' sources.cfg
sed -i 's/^ZODB/#ZODB/' sources.cfg
sed -i 's/^five./#five./' sources.cfg
sed -i 's/^z3c./#z3c./' sources.cfg
sed -i 's/^Products.CMF/#Products.CMF/' sources.cfg
sed -i 's/^Products.MailHost/#Products.MailHost/' sources.cfg
$PYTHON27 bootstrap.py --setuptools-version 33.1.1 --buildout-version 2.8.0 -c docs.cfg
bin/buildout -c docs.cfg install test

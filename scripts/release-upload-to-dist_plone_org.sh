#!/bin/bash
CFG="upload_to_dist.cfg"

git checkout $VERSION

mkdir -p release-cache/{eggs,downloads,extends}

cat > $CFG << EOF
[buildout]
extends = core.cfg

eggs-directory = release-cache/eggs
download-cache = release-cache/downloads
extends-cache = release-cache/extends

auto-checkout =
EOF

if [ "$VERSION" = "4.3" ];
then
    $PYTHON27 bootstrap.py -c ${CFG}
else
    $PYTHON27 bootstrap.py --setuptools-version 21.0.0 -c $CFG
fi
bin/buildout -c $CFG

echo "Uploading versions.cfg"
#scp versions.cfg dist.plone.org:XXX
echo "Uploading eggs"
#scp -r release-cache/downloads/dist/ dist.plone.org:XXX

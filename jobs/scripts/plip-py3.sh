#!/bin/bash
sed -i 's/    mr.developer/    mr.developer\ngit-clone-depth = 100/' core.cfg
pip install -r requirements.txt
buildout -c py3.cfg


cat > test.py << EOF
from plone import api
EOF

./bin/instance run test.py > output.txt

#!/usr/bin/env bash
# checkout all plone and collective org packages
cat > checkouts.cfg << EOF
[buildout]
git-clone-depth = 1
always-checkout = force
auto-checkout =
EOF

for pkg in `grep -E "remotes:(plone|collective)" sources.cfg | cut -d" " -f1 | sed 's/=//'`;
do
    echo "    ${pkg}" >> checkouts.cfg
done

# bootstrap and install z3c.dependencychecker
pip install -r requirements.txt
buildout -c core.cfg install dependencies

# get all dependencies
echo "" > deps.txt
for pkg in src/*;
do
    echo "$pkg" >> deps.txt
    ./bin/dependencychecker --exit-zero $pkg >> deps.txt || echo "Failed for $pkg"
done

LINES=`wc -l deps.txt | cut -d" " -f1`
echo "YVALUE=${LINES}" > lines.log
PKGS=`ls src/*/pyproject.toml | wc -l`
echo "YVALUE=${PKGS}" > pkgs.log

#!/usr/bin/env bash
# checkout only the package being tested
cat > checkouts.cfg << EOF
[buildout]
git-clone-depth = 1
always-checkout = force
auto-checkout =
    ${PACKAGE_NAME}
EOF

if grep "${PACKAGE_NAME}" sources.cfg | grep "${BRANCH}" > /dev/null
then
    echo "${PACKAGE_NAME} already has ${BRANCH} in sources.cfg"
else
    echo "branch of ${PACKAGE_NAME} has been changed to ${BRANCH} in sources.cfg"
    sed -i "s/\(${PACKAGE_NAME} .*branch=\)[a-z0-9]*/\1${BRANCH}/" sources.cfg
    grep "${PACKAGE_NAME}" sources.cfg
fi

pip install -Ur requirements.txt
buildout -c core.cfg install dependencies

return_code=0
./bin/dependencychecker src/${PACKAGE_NAME} > deps.txt || return_code=$?

if [ -f "src/${PACKAGE_NAME}/pyproject.toml" ];
then
  python templates/deps-update-status.py
fi

exit ${return_code}

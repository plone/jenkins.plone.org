if [ "{plone-version}" = "4.3" ]; then
    $PYTHON27 bootstrap.py -c jenkins.cfg
else
    $PYTHON27 bootstrap.py --setuptools-version=18.2 -c jenkins.cfg
fi
if [ "$COREDEV" = "1" ]; then
    # TODO(gforcada): allow to test remote branches (i.e. branches not in github.com/plone/buildout.coredev)
    git checkout $PULL_REQUEST_BRANCH
else
    bin/buildout -c jenkins.cfg install add-package-to-auto-checkout
    for pkg in $PKGS; do
        bin/add-package-to-auto-checkout $pkg
    done
fi
bin/buildout -c jenkins.cfg
bin/alltests --xml --all
if [ "{plone-version}" = "5.0" ]; then
    bin/alltests-at --xml
fi

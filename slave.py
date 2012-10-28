from fabric.api import *
from fabric.contrib.files import sed, append, exists, contains

env.user = 'timo'
env.hosts = [
    '152.19.4.89',
    '152.19.4.98',
]

env.home = "/home/jenkins"


def setup():
    """Set up slave for jenkins.plone.org.
    """
    # Update system
    sudo('apt-get update -y')
    sudo('apt-get dist-upgrade -y')
    sudo('apt-get autoremove -y')
    # Basics
    sudo('apt-get install -y build-essential')
    sudo('apt-get install -y htop')
    # Time sync
    sudo('apt-get install -y ntp')
    # VCS
    sudo('apt-get install -y git-core')
    sudo('apt-get install -y subversion')
    sudo('apt-get install -y libxml2-utils')
    # Word support
    sudo('apt-get install -y wv')
    # PDF support
    sudo('apt-get install -y poppler-utils')
    # X-server for robot tests
    sudo('apt-get install -y xvfb')
    # bz2 support to extract pypi packages
    sudo('apt-get install -y libbz2-dev')
    # Code analysis
    sudo('apt-get install -y ohcount')
    sudo('apt-get install -y sloccount')
    sudo('apt-get install -y nodejs npm')
    sudo('npm install -g jslint')
    sudo('npm install -g jshint')
    sudo('npm install -g csslint')

    setup_jenkins_user()
    setup_jenkins_ssh()
    setup_git_config()

    setup_python_26()
    setup_python_27()


def setup_git_config():
    """Set up a git configuration file (.gitconfig).
    """
    put('etc/.gitconfig', '/tmp')
    sudo('mv /tmp/.gitconfig /home/jenkins/')
    sudo('chown jenkins:jenkins /home/jenkins/.gitconfig')


def test_setup_python_26():
    """Test Python 2.6 setup.
    """
    with settings(warn_only=True):
        result = run('echo "print(True)" | python2.6')
    if result.failed:
        abort("Python 2.6 is not properly installed!")

    with settings(warn_only=True):
        result = run('echo "import hashlib" | python2.6')
    if result.failed:
        abort("Python 2.6: Haslib is not properly installed!")

    with settings(warn_only=True):
        run('echo "import lxml" | python2.6')
    if result.failed:
        abort("Python 2.6: LXML is not properly installed!")

    with settings(warn_only=True):
        run('echo "import _imaging" | python2.6')
    if result.failed:
        abort("Python 2.6: PIL is not properly installed!")

    with settings(warn_only=True):
        sudo('echo "from urllib import urlopen; from cStringIO import StringIO; from PIL import Image; Image.open(StringIO(urlopen(\'http://plone.org/logo.jpg\').read()))" | python2.6')
    if result.failed:
        abort("Python 2.6: PIL JPEG support is not properly installed!")

    with settings(warn_only=True):
        sudo('echo "from urllib import urlopen; from cStringIO import StringIO; from PIL import Image; Image.open(StringIO(urlopen(\'http://plone.org/logo.png\').read()))" | python2.6')
    if result.failed:
        abort("Python 2.6: PIL PNG support is not properly installed!")


def setup_python_26():
    """Install Python 2.6 with Imaging and LXML.
    """
    # http://ubuntuforums.org/showthread.php?t=1976837
    if exists('/opt/python-2.6', use_sudo=True):
        sudo('rm -rf /opt/python-2.6')
    if exists('/root/tmp', use_sudo=True):
        sudo('rm -rf /root/tmp')
    sudo('mkdir /root/tmp')
    with cd('/root/tmp'):
        sudo('wget http://python.org/ftp/python/2.6.8/Python-2.6.8.tgz')
        sudo('tar xfvz Python-2.6.8.tgz')
    with cd('/root/tmp/Python-2.6.8/'):
        put('etc/setup.py.patch', '/tmp')
        sudo('patch setup.py < /tmp/setup.py.patch')
        put('etc/ssl.patch', '/tmp')
        sudo('patch Modules/_ssl.c < /tmp/ssl.patch')
        sudo('env CPPFLAGS="-I/usr/lib/x86_64-linux-gnu" LDFLAGS="-L/usr/include/x86_64-linux-gnu" ./configure --prefix=/opt/python2.6')
        sudo('make')
        put('etc/ssl.py.patch', '/tmp')
        sudo('patch Lib/ssl.py < /tmp/ssl.py.patch')
        sudo('make install')
    # PIL
    sudo('apt-get install -y zlib1g-dev')
    sudo('apt-get install -y libfreetype6 libfreetype6-dev')
    sudo('apt-get install -y libjpeg-dev')
    #http://www.sandersnewmedia.com/why/2012/04/16/installing-pil-virtualenv-ubuntu-1204-precise-pangolin/
    if not exists('/usr/lib/`uname -i`-linux-gnu/libfreetype.so'):
        sudo('ln -s /usr/lib/`uname -i`-linux-gnu/libfreetype.so /usr/lib/')
    if not exists('/usr/lib/`uname -i`-linux-gnu/libjpeg.so'):
        sudo('ln -s /usr/lib/`uname -i`-linux-gnu/libjpeg.so /usr/lib/')
    if not exists('/usr/lib/`uname -i`-linux-gnu/libz.so'):
        sudo('ln -s /usr/lib/`uname -i`-linux-gnu/libz.so /usr/lib/')
    with cd('/root/tmp'):
        sudo('wget http://effbot.org/downloads/Imaging-1.1.7.tar.gz')
        sudo('tar xfvz Imaging-1.1.7.tar.gz')
    with cd('/root/tmp/Imaging-1.1.7/'):
        sudo('/opt/python2.6/bin/python setup.py install')
    # Install BZ2 Support
    with cd('/root/tmp'):
        sudo('wget http://labix.org/download/python-bz2/python-bz2-1.1.tar.bz2')
        sudo('tar xfvj python-bz2-1.1.tar.bz2')
    with cd('/root/tmp/python-bz2-1.1/'):
        sudo('/opt/python2.6/bin/python setup.py install')
    # Install LXML
    sudo('apt-get install -y libxslt1-dev libxml2-dev')
    with cd('/root/tmp'):
        sudo('wget http://pypi.python.org/packages/source/l/lxml/lxml-2.3.6.tar.gz')
        sudo('tar xfvz lxml-2.3.6.tar.gz')
    with cd('/root/tmp/lxml-2.3.6/'):
        sudo('/opt/python2.6/bin/python setup.py install')
    # Create Symlink
    if not exists('/usr/local/bin/python2.6'):
        sudo('ln -s /opt/python2.6/bin/python /usr/local/bin/python2.6')
    # Clean up
    sudo('rm -rf /root/tmp')
    # Distribute
    sudo('curl http://python-distribute.org/distribute_setup.py | python2.6')
    test_setup_python_26()


def test_setup_python_27():
    """Test Python 2.7 setup.
    """
    with settings(warn_only=True):
        result = run('echo "print(True)" | python2.7')
    if result.failed:
        abort("Python 2.7 is not properly installed!")

    with settings(warn_only=True):
        result = run('echo "import hashlib" | python2.7')
    if result.failed:
        abort("Python 2.7: Haslib is not properly installed!")

    with settings(warn_only=True):
        run('echo "import lxml" | python2.7')
    if result.failed:
        abort("Python 2.7: LXML is not properly installed!")

    with settings(warn_only=True):
        run('echo "import _imaging" | python2.7')
    if result.failed:
        abort("Python 2.7: PIL is not properly installed!")


def setup_python_27():
    """Install Python 2.7 with Imaging and LXML.
    """
    sudo('apt-get install -y python2.7')
    sudo('apt-get install -y python2.7-dev')
    # Distribute
    sudo('curl http://python-distribute.org/distribute_setup.py | python')
    # PIL
    sudo('apt-get install -y python-imaging')
    # LXML
    sudo('apt-get install -y python-lxml')
    # Test Coverage
    sudo('apt-get install -y enscript')
    test_setup_python_27()


def setup_jenkins_user():
    """Set up jenkins user.
    """
    if not exists('/home/jenkins', use_sudo=True):
        sudo('adduser jenkins --disabled-password --home=/home/jenkins')


def setup_buildout_cache():
    if not exists('/home/jenkins/.buildout/'):
        sudo('mkdir /home/jenkins/.buildout', user='jenkins')
        sudo('mkdir /home/jenkins/.buildout/eggs', user='jenkins')
        sudo('mkdir /home/jenkins/.buildout/downloads', user='jenkins')
    if exists('/home/jenkins/.buildout/default.cfg'):
        sudo('rm /home/jenkins/.buildout/default.cfg', user='jenkins')
    put('etc/default.cfg', '/tmp/')
    sudo('cp /tmp/default.cfg /home/jenkins/.buildout/', user='jenkins')


def setup_jenkins_ssh():
    """Set up ssh key.
    """
    if not exists('/home/jenkins/.ssh', use_sudo=True):
        sudo('mkdir /home/jenkins/.ssh', user='jenkins')
    if not exists('/home/jenkins/.ssh/authorized_keys', use_sudo=True):
        with cd('/home/jenkins/.ssh'):
            sudo(
                'wget https://raw.github.com/plone/jenkins.plone.org/master/jenkins.plone.org.pub',
                user='jenkins'
            )
            sudo('touch authorized_keys', user='jenkins')
            sudo(
                'cat jenkins.plone.org.pub >> authorized_keys', user='jenkins'
            )
            sudo('rm jenkins.plone.org.pub', user='jenkins')
            sudo(
                'chmod g-w /home/jenkins/ /home/jenkins/.ssh /home/jenkins/.ssh/authorized_keys',
                user='jenkins'
            )


# HELPER ---------------------------------------------------------------------

def _sudo_put(source, destination, user):
    put(source, '/tmp')
    sudo('mv /tmp/%s %s' % (source, destination))
    sudo('chown user:user %s' % (user, user, destination))


# TODO -----------------------------------------------------------------------

def setup_gil_user():
    """TODO. This should be more generic. All admins need an account.
    """
    if not exists('/home/gil', use_sudo=True):
        sudo('adduser gil --disabled-password --home=/home/gil')
    sudo('adduser gil sudo')
    # TODO: create ssh setup with public key of that user


def setup_eggproxy():
    """Set up collective.eggproxy to make the buildouts faster.
    """
    pass


def setup_munin():
    """Set up munin.
    """
    sudo('apt-get install -y munin munin-node')
    put('etc/munin.conf', '/etc/munin/munin.conf')
    put('etc/munin-node.conf', '/etc/munin/munin-node.conf')
    sudo('/etc/init.d/munin-node restart')
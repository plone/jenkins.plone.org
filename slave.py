from fabric.api import *
from fabric.contrib.files import sed, append, exists, contains

env.user = 'timo'
env.hosts = [
    '152.19.4.89',
#    '152.19.4.98',
]

env.home = "/home/jenkins"


def setup():
    """Set up slave for jenkins.plone.org.
    """
    sudo('apt-get update')
    sudo('apt-get dist-upgrade')
    sudo('apt-get autoremove')
    sudo('apt-get install -y build-essential')
    sudo('apt-get install -y htop')
    sudo('apt-get install -y ntp')
    sudo('apt-get install -y git-core')
    sudo('apt-get install -y subversion')
    sudo('apt-get install -y libxml2-utils')
    sudo('apt-get install -y nodejs npm')
    sudo('npm install -g jslint')
    sudo('apt-get install -y wv')
    sudo('apt-get install -y xvfb')
    sudo('apt-get install libbz2-dev')

    setup_git_config()
    setup_python_26()
    setup_python_27()
    setup_jenkins_user()
    setup_jenkins_ssh()


def setup_git_config():
    """Set up a git configuration file (.gitconfig).
    """
    put('etc/.gitconfig', '/home/jenkins/.gitconfig', use_sudo=True)
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
        put('etc/setup.py.patch', '/root/tmp/Python-2.6.8/setup.py.patch', use_sudo=True)
        sudo('patch setup.py < setup.py.patch')
        put('etc/ssl.patch', '/root/tmp/Python-2.6.8/ssl.patch', use_sudo=True)
        sudo('patch Modules/_ssl.c < ssl.patch')
        sudo('env CPPFLAGS="-I/usr/lib/x86_64-linux-gnu" LDFLAGS="-L/usr/include/x86_64-linux-gnu"  ./configure --prefix=/opt/python2.6')
        sudo('make')
        put('etc/ssl.py.patch', '/root/tmp/Python-2.6.8/ssl.py.patch', use_sudo=True)
        sudo('patch Lib/ssl.py < ssl.py.patch')
        sudo('make install')
    # Install PIL
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
    sudo('apt-get install -y zlib1g-dev')
    sudo('apt-get install -y libfreetype6 libfreetype6-dev')
    sudo('apt-get install -y libjpeg62 libjpeg62-dev')
    # LXML
    sudo('apt-get install -y python-lxml')
    sudo('apt-get install -y libxslt1-dev libxml2-dev')
    # Test Coverage
    sudo('apt-get install enscript')
    test_setup_python_27()


def setup_jenkins_user():
    """Set up jenkins user.
    """
    if not exists('/home/jenkins', use_sudo=True):
        sudo('adduser jenkins --disabled-password --home=/home/jenkins')


def setup_jenkins_ssh():
    """Set up ssh key.
    """
    if not exists('/home/jenkins/.ssh', use_sudo=True):
        sudo('mkdir /home/jenkins/.ssh', user='jenkins')
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
    pass

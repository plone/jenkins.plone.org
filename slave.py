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
    sudo('apt-get install -y ntp')
    sudo('apt-get install -y git-core')
    sudo('apt-get install -y subversion')
    sudo('apt-get install -y libxml2-utils')
    sudo('apt-get install -y nodejs npm')
    sudo('npm install -g jslint')
    sudo('apt-get install -y wv')
    setup_python_26()
    setup_python_27()
    setup_jenkins_user()
    setup_jenkins_ssh()


def setup_python_26():
    """Install Python 2.6 with Imaging and LXML.
    """
    # http://lipyrary.blogspot.de/2011/05/how-to-compile-python-on-ubuntu-1104.html
    if not exists('/root/tmp', use_sudo=True):
        sudo('mkdir /root/tmp')

    with cd('/root/tmp'):
        sudo('wget http://python.org/ftp/python/2.6.8/Python-2.6.8.tgz')
        sudo('tar xfvz Python-2.6.8.tgz')
    with cd('/root/tmp/Python-2.6.8/'):
        sudo('export LDFLAGS="-L/usr/lib/$(dpkg-architecture -qDEB_HOST_MULTIARCH)"')
        sudo('./configure --prefix=/opt/python-2.6/')
        sudo('make')
        sudo('make install')
        sudo('unset LDFLAGS')
    with cd('/root/tmp'):
        sudo('wget http://effbot.org/downloads/Imaging-1.1.7.tar.gz')
        sudo('tar xfvz Imaging-1.1.7.tar.gz')
    with cd('/root/tmp/Imaging-1.1.7/'):
        sudo('/opt/python-2.6/bin/python setup.py install')
    with cd('/root/tmp'):
        sudo('rm -rf Python-2.6.8*')
        sudo('rm -rf Imaging-1.1.7*')
        sudo('rm -rf /root/tmp')
    if not exists('/usr/local/bin/python2.6'):
        sudo('ln -s /opt/python-2.6/bin/python /usr/local/bin/python2.6')


def test_setup_python_27():
    run('echo "print("\ok"\)" | python2.7')
    run('echo "import lxml" | python2.7')
    run('echo "import _imaging" | python2.7')


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

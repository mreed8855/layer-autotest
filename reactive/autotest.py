import os
import distutils.dir_util
import shutil

from charmhelpers.core import hookenv
from charmhelpers.core.hookenv import status_set 
from charmhelpers.fetch import install_remote

from charms import reactive
from charms.reactive import (
    hook,
    when,
    when_not,
    set_state,
)


config = hookenv.config()
charm_dir = hookenv.charm_dir()

autotest_server = config.get('autotest-server')
autotest_client = config.get('autotest-client')
autotest_dir = os.path.join(hookenv.charm_dir(), ".tmp/autotest")
autotest_client_test_dir = os.path.join(autotest_dir, "client/tests")
os.environ["AUTODIR"] = autotest_dir


@when_not("autotest.installed")
def install_autotest():
    '''
    Install the needed packages for autotest
    Clone autotest server and client directory
    '''

    setup_autotest()
    setup_custom_client_tests()
    set_state("autotest.installed")

@hook('config-changed')
def config_changed():
    '''
    Add custom tests to the client test directory
    '''
    if config.changed('autotest-custom-tests'):
        setup_custom_client_tests()
        hookenv.log('config-changed custom tests updated')


@when("autotest.installed")
def set_autotest_state():
    status_set('active', 'Autotest is Ready')

def git_clone(src, destination):
    '''
    Use install_remote to clone git repos
    '''

    cloned_dir = None
    cloned_dir = install_remote(src, dest=destination,
                                branch='master', depth=None)

    return cloned_dir


def setup_autotest():
    '''
    Install the server and client tests from git repos
    '''

    autotest_server_dir = git_clone(autotest_server, hookenv.charm_dir())
    autotest_client_dir = git_clone(autotest_client, hookenv.charm_dir())

    distutils.dir_util.copy_tree(autotest_server_dir, autotest_dir)
    distutils.dir_util.copy_tree(autotest_client_dir, autotest_client_test_dir)

    shutil.rmtree(autotest_server_dir)
    shutil.rmtree(autotest_client_dir)


def setup_custom_client_tests():
    if config.get('autotest-custom-tests'):
        autotest_custom_tests = config.get('autotest-custom-tests')
        autotest_custom_dir = git_clone(autotest_custom_tests,
                                        hookenv.charm_dir())
        distutils.dir_util.copy_tree(autotest_custom_dir,
                                     autotest_client_test_dir)
        shutil.rmtree(autotest_custom_dir)

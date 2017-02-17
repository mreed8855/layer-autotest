import os
import distutils.dir_util
import shutil

from charmhelpers.core import hookenv
from charmhelpers.fetch import install_remote
from charms import apt
from charms import reactive

from charms.reactive import (
    hook,
    set_state,
    is_state,
    when_not,
    when,
    when_any,
)

config = hookenv.config()
charm_dir = hookenv.charm_dir()

autotest_server = config.get('autotest-server')
autotest_client = config.get('autotest-client')
autotest_dir = os.path.join(hookenv.charm_dir(), ".tmp/autotest")
autotest_client_test_dir = os.path.join(autotest_dir, "client/tests")
os.environ["AUTODIR"] = autotest_dir

@hook('install')
def install_autotest():
    '''
    Install the needed packages for autotest
    Clone autotest server and client directory
    '''
    packages = [
        'gcc', 
        'dh-autoreconf', 
        'autoconf', 
        'python-pexpect', 
        'libkeyutils-dev', 
        'libattr1-dev', 
        'automake',
        'build-essential',
        'gdb',
        'git',
    ]
    

    apt.queue_install(packages)
    apt.install_queued()


    autotest_server_dir = git_clone(autotest_server, hookenv.charm_dir())
    autotest_client_dir = git_clone(autotest_client, hookenv.charm_dir())    
    
    distutils.dir_util.copy_tree(autotest_server_dir, autotest_dir)
    distutils.dir_util.copy_tree(autotest_client_dir, autotest_client_test_dir)
    
    shutil.rmtree(autotest_server_dir)  
    shutil.rmtree(autotest_client_dir)  

@hook('config-changed')
def config_changed():
    '''
    Add custom tests to the client test directory
    '''
    if config.changed('autotest-custom-tests'):
       autotest_custom_tests =  config.get('autotest-custom-tests')
       autotest_custom_dir = git_clone(autotest_custom_tests, hookenv.charm_dir())
       distutils.dir_util.copy_tree(autotest_custom_dir, autotest_client_test_dir)
       shutil.rmtree(autotest_custom_dir)
       hookenv.log('config-changed updated')     

# Used for debug
#    hookenv.log('************************')
#    hookenv.log('config-changed called')     
#    hookenv.log('************************')
    

def git_clone(src, destination):
    '''
    Use install_remote to clone git repos 
    '''
    
    cloned_dir = None
    cloned_dir = install_remote(src, dest=destination,
                                  branch='master', depth=None)

    return cloned_dir

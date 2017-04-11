#Overview
Updated for JuJu 2.0

The Autotest Charm creates a flexible method for running testcases inside the Autotest(autotest-local)  Framework using juju actions.  
The source for these tests are currently git://kernel.ubuntu.com/ubuntu/autotest but these can be changed to other git repos.  
 
##Usage:

    juju bootstrap
    juju deploy autotest

Tests are execute using juju actions.  Current available tests:

* dbench
* stress
* stress_ng  - Stress-ng (long running test, it takes approximately 3 hours to complete)
* ubuntuqrt  - QA Regression Tests - (disabled by default)
* custom     - currently sleeptest.  This can be changed to any tests located in the autotest-client-tests directory.  sleeptest is a short and simple test that is similar to a smoke test
The available tests can be found in autotest/actions directory

##Listing the Tests

    juju list-actions autotest

##Running the Tests

    juju run-action autotest/0  dbench

This returns an job id that can be used to wait for the completion of the test

* Fetch the status of the test

    juju show-action-status <ID>

* Fetch the results of the test

    juju show-action-output <ID>

#Adding Client Tests

##Create a test in the autotest format and set and create a git repository. The following link documents how to create tests

    http://autotest.readthedocs.io/en/latest/main/local/AddingTest.html

##Conifgure autotest-custom-tests to point to a reposistory that contains 

    juju config autotest autotest-custom-tests='https://github.com/mreed8855/custom-tests.git'

##Running the Newly Added tests with actions

    juju run-action autotest/* custom testnames='testname1 testname2 ..."


Results are moved to the $CHARM_DIR/.tmp/results/$test-name after each run. 

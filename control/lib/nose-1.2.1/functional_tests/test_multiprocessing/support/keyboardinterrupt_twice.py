import os

from tempfile import mktemp
from time import sleep

if 'NOSE_MP_LOG' not in os.environ:
    raise Exception('Environment variable NOSE_MP_LOG is not set')

logfile = os.environ['NOSE_MP_LOG']

def log(w):
    f = open(logfile, 'a')
    f.write(w+"\n")
    f.close()
#make sure all tests in this file are dispatched to the same subprocess
def setup():
    '''global logfile
    logfile = mktemp()
    print "tempfile is:",logfile'''
    log('setup')

def test_timeout():
    log('test_timeout')
    sleep(2)
    log('test_timeout_finished')

# check timeout will not prevent remaining tests dispatched to the same subprocess to continue to run
def test_pass():
    log('test_pass')

def teardown():
    log('teardown')
    sleep(10)
    log('teardown_finished')

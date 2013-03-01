'''
Created on Feb 28, 2013

@author: joshandrews
'''
from setuptools.command import easy_install
from os import path
import sys
import os

# Any library dependencies must be added here
LIB_DEPENDENCIES = ['mock == 1.0.1', 'pyserial == 2.6', 'nose']
# Name of top level directory
TEST_PACKAGE = "control"
SETUP_OPTIONS = {"install_lib":"Installs all library dependencies", 
                 "test":"Finds and runs all project unit tests",
                 "install":"Installs dependencies"}

    
def install_lib():
    print ("Installing all library dependencies")
    easy_install.main(LIB_DEPENDENCIES)

def test():
    print('Running UBC Sailbot Control Tests')
    nose_installed = True
    try: 
        import nose
    except ImportError: 
        easy_install.main(['nose'])
        nose_installed = False
    if (nose_installed):
        suite_1 = nose.loader.TestLoader().loadTestsFromName(TEST_PACKAGE)
        nose.run(suite=suite_1)
    else:
        print("\n Installed missing dependencies.  Rerun test script \n")

def install():
    install_lib()
    
def printOptions():
    print("usage: setup.py [arg]")
    print("arg options:")
    for key, value in SETUP_OPTIONS.iteritems():
        print("    " + key + " : " + value)
    print("")
    
def main():    
    if (len(sys.argv) > 1):
        try:
            globals()[sys.argv[1]]()
        except KeyError:
            print ("Invalid Argument")
            printOptions()
    else:
        printOptions()

if __name__ == '__main__':
    sys.exit(main())

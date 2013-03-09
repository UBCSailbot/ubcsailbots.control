'''
Created on Feb 28, 2013

@author: joshandrews
'''
from os import path
import sys
import os
from control import ez_setup
try:
    from setuptools.command import easy_install
except ImportError:
    print "\n Installed missing dependencies.  Rerun \n"    
    ez_setup.main()
    sys.exit()
    

# Any library dependencies must be added here
LIB_DEPENDENCIES = ['mock == 1.0.1', 'pyserial == 2.6', 'nose == 1.2.1']
# Name of top level directory
TEST_PACKAGE = "control"
# Setup options - any added functionality must be added here
SETUP_OPTIONS = {
                 "install_lib":"Installs all library dependencies", 
                 "test":"Finds and runs all project unit tests",
                 "install":"Installs dependencies"
                 }


# Installs all library dependencies defined in the LIB_DEPENDENCIES list
def install_lib():
    print ("Installing all library dependencies")        
    easy_install.main(LIB_DEPENDENCIES)

# Uses the nose library to run unit tests.  Installs missing dependencies.
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

# Prints setup.py options 
def printOptions():
    print("usage: setup.py [arg]")
    print("arg options:")
    for key, value in SETUP_OPTIONS.iteritems():
        print("    " + key + " : " + value)
    print("")
    
def main():    
    # Runs the argument as a function, catches invalid argument
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

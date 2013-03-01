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

if (sys.argv[1] == "install_lib"):
    print ("Installing all library dependencies")
    easy_install.main(LIB_DEPENDENCIES)



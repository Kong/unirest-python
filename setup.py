'''
Created on Dec 13, 2012

@author: mashape
'''
#!/usr/bin/env python

from distutils.core import setup

setup(name='mashape-client-lib',
      version='1.0',
      description='Mashape client library',
      author='Mashape Inc.',
      author_email='support@mashape.com',
      url='https://github.com/Mashape/mashape-python-client-library/',
      packages = ['mashape', 'mashape.auth', 'mashape.config','mashape.exception','mashape.http'],
     )

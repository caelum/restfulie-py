#!/usr/bin/python

from setuptools import setup

setup(name='restfulie',
      version='0.8',
      namespace_packages = ['restfulie'],
      test_suite = "nose.collector",
      install_requires= ['httplib2>=0.6.0'],
      setup_requires=['nose>=0.11'],
      tests_require=[ 'mockito>=0.5.1'],
      packages=['restfulie'])


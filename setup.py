#!/usr/bin/python

from setuptools import setup

setup(name='restfulie',
      version='0.8.0',
      description='Writing hypermedia aware resource based clients and servers',
      author=' ',
      author_email=' ',
      url='http://restfulie.caelumobjects.com/',
      long_description='CRUD through HTTP is a good step forward to using resources and becoming RESTful, another step further is to make use of hypermedia aware resources and Restfulie allows you to do it in Python.',
      download_url='https://github.com/caelum/restfulie-py',
      keywords='restfulie rest http hypermedia',
      classifiers=[
          "Development Status :: 4 - Beta",
          "Environment :: Web Environment",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: Apache Software License",
          "Operating System :: MacOS :: MacOS X",
          "Operating System :: Microsoft :: Windows",
          "Operating System :: POSIX",
          "Programming Language :: Python",
      ],
      test_suite = "nose.collector",
      install_requires= ['httplib2>=0.6.0'],
      setup_requires=['nose>=0.11'],
      tests_require=[ 'mockito>=0.5.1'],
      packages=['restfulie'])


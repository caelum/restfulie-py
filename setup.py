from setuptools import setup

setup(name='restfulie',
      version='0.1',
      namespace_packages = ['restfulie'],
      test_suite = "nose.collector",
      setup_requires=['nose>=0.11', 'mockito>=0.5.1'],
      packages=['restfulie'])


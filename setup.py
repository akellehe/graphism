try:
  from setuptools import setup, find_packages
except ImportError:
  import distribute_setup
  distribute_setup.use_setuptools()
  from setuptools import setup, find_packages

setup(
  name='graphism',
  version='1.0.1',
  packages=find_packages(),
  author='Andrew Kelleher',
  author_email='akellehe@gmail.com',
  description='Basic network graph test package',
  test_suite='graphism.tests'
)

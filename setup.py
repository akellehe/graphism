try:
  from setuptools import setup, find_packages
except ImportError:
  import distribute_setup
  distribute_setup.use_setuptools()
  from setuptools import setup, find_packages

setup(
  name='graphism',
  version='1.0.4',
  packages=find_packages(),
  author='Andrew Kelleher',
  author_email='akellehe@gmail.com',
  description='Basic network graph test package',
  test_suite='graphism.tests',
  install_requires=[
    "Jinja2==2.6",
    "Pygments==1.6",
    "Sphinx==1.2b1",
    "docutils==0.10",
    "pyglet==1.1.4",
    "wsgiref==0.1.2"
  ]

)

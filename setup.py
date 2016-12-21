from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

setup(name              = 'escape-pi',
      version           = '1.0.0',
      author            = 'Boyko Kazakov',
      author_email      = 'boikonur@gmail.com',
      description       = 'Wall GUI for RPI',
      license           = 'GNU GPLv2',
      url               = 'https://github.com/boikonur/escape-pi',
      install_requires  = ['pyudev'],
      packages          = find_packages())
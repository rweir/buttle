#!/usr/bin/env python

from setuptools import setup

from buttle import __version__

setup(name='Buttle',
      version=__version__,
      description='Big Brother DataBase parser',
      author='Rob Weir',
      author_email='rweir@ertius.org',
      url='http://ertius.org/code/buttle/',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Text Editors :: Emacs',
        'Topic :: Communications :: Email :: Address Book',
        'Intended Audience :: Developers',
        ],
      packages=['buttle'],
     )

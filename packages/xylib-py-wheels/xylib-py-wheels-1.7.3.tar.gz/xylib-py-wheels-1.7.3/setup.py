#!/usr/bin/env python

# This setup.py builds xylib as a python extension, which is experimental.
# The normal way of building xylib is using configure && make. Or cmake.
long_description="""\
This package contains built wheels for xylib by Marcin Wojdyr (https://github.com/wojdyr/xylib)
xylib is a library for reading obscure file formats with data from
powder diffraction, spectroscopy and other experimental methods.
For the list of supported formats see https://github.com/wojdyr/xylib .

This module includes bindings to xylib and xylib itself.
The first two numbers in the version are the version of included xylib.
"""
from setuptools import setup
from distutils.core import Extension
from distutils.command.sdist import sdist
from glob import glob
import sys

# as per http://stackoverflow.com/a/21236111/104453
from distutils.command.build import build
class CustomBuild(build):
    sub_commands = [('build_ext', build.has_ext_modules),
                    ('build_py', build.has_pure_modules),
                    ('build_clib', build.has_c_libraries),
                    ('build_scripts', build.has_scripts)]

sources = glob('xylib/*.cpp') + ['xylib.i']

swig_opts = ['-c++', '-modern', '-modernargs']
if sys.version_info[0] == 3:
    swig_opts += ['-py3']

setup(name='xylib-py-wheels',
      version='1.7.3',
      description='Built wheels for xylib by Marcin Wojdyr',
      long_description=long_description,
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'Programming Language :: Python :: Implementation :: CPython',
          'Topic :: Scientific/Engineering :: Chemistry',
          'Topic :: Software Development :: Libraries :: Python Modules',
          ],
      author='Christopher Stallard',
      author_email='christopher.stallard1@gmail.com',
      license='LGPL2.1',
      url='https://github.com/wojdyr/xylib',
      ext_modules=[Extension('_xylib',
                             sources=sources,
                             language='c++',
                             swig_opts=swig_opts,
                             include_dirs=['.'],
                             libraries=[])],
      py_modules=['xylib'],
      cmdclass={'build': CustomBuild})

#!/usr/bin/env python3
import os
import sys
try:
    from setuptools import setup
    from setuptools.command.install import install as _install
    from setuptools.command.sdist import sdist as _sdist
except ImportError:
    from distutils.core import setup
    from distutils.command.install import install as _install
    from distutils.command.sdist import sdist as _sdist


# https://github.com/eliben/pycparser/blob/master/setup.py
def _run_build_tables(directory):
    from subprocess import check_call
    # This is run inside the install staging directory (that had no .pyc files)
    # We don't want to generate any.
    # https://github.com/eliben/pycparser/pull/135
    check_call([sys.executable, '-B', '_build_tables.py'],
               cwd=os.path.join(directory, 'pycparserext_gnuc'))


class install(_install):
    def run(self):
        _install.run(self)
        self.execute(_run_build_tables, (self.install_lib,),
                     msg="Build the lexing/parsing tables")


class sdist(_sdist):
    def make_release_tree(self, basedir, files):
        _sdist.make_release_tree(self, basedir, files)
        self.execute(_run_build_tables, (basedir,),
                     msg="Build the lexing/parsing tables")

setup(name="pycparserext_gnuc",
      version="2022.10",
      description="GNU C extension for pycparser, based on inducer/pycparseext",
      long_description=open("README.rst", "r").read(),
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Intended Audience :: Other Audience',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Programming Language :: Python',
          'Topic :: Utilities',
          ],

      python_requires=">=3.6",
      install_requires=[
          "ply>=3.4",
          "pycparser>=2.18",
          ],

      author="Andreas Kloeckner",
      url="http://pypi.python.org/pypi/pycparserext",
      author_email="inform@tiker.net",
      license="MIT",
      packages=["pycparserext_gnuc"],
      cmdclass={'install': install, 'sdist': sdist}
)

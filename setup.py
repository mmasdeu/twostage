## -*- encoding: utf-8 -*-
import os
import sys
import re
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
from setuptools import setup
from codecs import open # To open the README file with proper encoding
from setuptools.command.test import test as TestCommand # for tests
from distutils.command import build as build_module

# Obtain the different Sage versions
def get_all_version_names(mirror_url, idx = None, distribution = 'Ubuntu_12.04-x86_64'):
    if idx is None:
        idx = 0
    else:
        idx = int(idx)
    site = urlopen(mirror_url).read()
    ans = re.findall('(sage-([0-9]*(?:\.[0-9]*)*)-%s.tar.bz2)'%distribution, site)
    all_version_names = []
    for fname, ver in ans:
        if fname not in all_version_names:
            all_version_names.append(fname)
    return all_version_names[idx]

# Get information from separate files (README, VERSION)
def readfile(filename):
    with open(filename,  encoding='utf-8') as f:
        return f.read()

# Check the right Sage version
class build(build_module.build):
    def run(self):
        from sagemath.check_version import check_version
        check_version(sage_required_version)
        build_module.build.run(self)

# For the tests
class SageTest(TestCommand):
    def run_tests(self):
        errno = os.system("sage -t --force-lib twostage")
        if errno != 0:
            sys.exit(1)

if __name__ == "__main__":
    # Specify the required Sage version
    sage_required_version = '>=7.5'

    setup(
        name = "twostage",
        version = readfile("VERSION"), # the VERSION file is shared with the documentation
        description='Algorithms for proving that class-number-one real quadratic fields are 2-stage euclidean, and to find continued fraction expansions in them.',
        long_description = readfile("README.rst"), # get the long description from the README
        url='https://github.com/mmasdeu/twostage',
        author='Xavier Guitart, Marc Masdeu',
        author_email='marc.masdeu@gmail.com', # choose a main contact email
        license='GPLv2+', # This should be consistent with the LICENCE file
        classifiers=[
          # How mature is this project? Common values are
          #   3 - Alpha
          #   4 - Beta
          #   5 - Production/Stable
          'Development Status :: 4 - Beta',
          'Intended Audience :: Science/Research',
          'Topic :: Scientific/Engineering :: Mathematics',
          'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
          'Programming Language :: Python :: 2.7',
        ], # classifiers list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        keywords = "euclidean, continued fractions, two stage, real quadratic",
        install_requires = ['sagemath'], # This ensures that Sage is installed
        packages = ['twostage'],
        include_package_data = True,
        cmdclass = {'build': build, 'test': SageTest} # adding a special setup command for tests
    )

import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages
from pip._vendor.requests import packages
from _ast import keyword

setup(
    name='FundamentalFactors',
    version='0.1',
    packages=['getfactors'],
    package_dir={'getfactors': 'src/getfactors'},
    scripts=['bin/commandline.sh'],
    package_data={
                  'getfactors': ['data/cfgs/*', 'data/example_trace/*'],
                  },
     # metadata for uptoad to PyPI  
    author = 'Barcelona Supercomputing Center (BSC-CNS)',
    author_email = 'crosas@bsc.es',
    description = 'Extracts fundamental factors from Paraver traces',
    long_description = open('README.txt').read(),
    license = "MIT",
    keywords = "fundamental factors performance analysis exascale",  
    url = 'http://www.bsc.es'
 )

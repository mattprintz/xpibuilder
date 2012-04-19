from setuptools import setup, find_packages
import sys, os

VERSION = '0.1.0'

setup(
    name='xpibuilder',
    version=VERSION,
    description='This module builds Mozilla extensions and packages them as .xpi files',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2 :: Only",
        "Topic :: Software Development :: Build Tools",
        "Intended Audience :: Developers",
        ], 
    keywords='mozilla xpi extension skin firefox thunderbird',
    author='Matthew Printz',
    author_email='matt.printz@rackspace.com',
    url='https://github.com/mattprintz/xpibuilder',
    license='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "rdflib",
        ],
    )

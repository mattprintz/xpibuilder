from setuptools import setup, find_packages
import sys, os

VERSION = '0.0.1'

setup(name='xpibuilder',
    version=VERSION,
    description='',
    classifiers=[], 
    keywords='',
    author='Matthew Printz',
    author_email='matt.printz@rackspace.com',
    url='',
    license='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "hashlib",
        "rdflib",
        ],
    setup_requires=[
        ],
    test_suite='',
    entry_points="""
    """,
    namespace_packages=[
        ],
    )

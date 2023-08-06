#!/usr/bin/env python

from setuptools import find_packages, setup

f = open('README.md', 'r')
long_description = f.read()


setup(
    name='geneplot',
    #packages=find_packages(include=['geneplot']),
    #packages=["geneplot"],
    include_package_data=True,
    version='1.0.0',
    description='Plot gene intron/exon topology, protein domains and SNPs',
    long_description=long_description, # here the README file goes
    long_description_content_type="text/markdown",
    url="https://github.com/gonzalezibeas/geneplot",
    author='Daniel',
    author_email="danielglz@mailfence.com",
    license='GPL',
    install_requires=['gffutils', 'Biopython', 'reportlab', 'matplotlib'],
    #setup_requires=['pytest-runner'],
    #tests_require=['pytest==4.4.1'],
    #test_suite='tests',

    #packages=find_packages(where="src"),
    #package_dir={"": "src"},
    #package_data={"mypkg": ["*.txt", "*.rst"]}


)



# commands to be run from the parent folder to compile
# python geneplot/setup.py sdist bdist_wheel
# check up the distribution
# twine check dist/*

# commands to be run to install
# pip install /path/to/wheelfile.whl




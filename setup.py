import os

from setuptools import find_packages, setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def requirements(fname):
    return [line.strip()
            for line in open(os.path.join(os.path.dirname(__file__), fname))]

setup(
    name = "mwcites",
    version = read('VERSION').strip(),
    author = "Aaron Halfaker",
    author_email = "ahalfaker@wikimedia.org",
    description = "A collection of scripts and utilities for extracting " +
                  "citations to academic literature from Wikipedia's XML " +
                  "database dumps.",
    license = "MIT",
    url = "https://github.com/halfak/Extract-scholarly-article-citations-from-Wikipedia",
    packages=find_packages(),
    entry_points = {
        'console_scripts': [
            'mwcitations=mwcites.mwcitations:main'
        ],
    },
    long_description = read('README.rst'),
    install_requires = ['docopt'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Science/Research",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
        "Topic :: Scientific/Engineering"
    ]
)

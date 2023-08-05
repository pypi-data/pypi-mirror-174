# Installation script for python
from setuptools import setup, find_packages
import os
import re

PACKAGE = "getcf"
here = os.path.abspath(os.path.dirname(__file__))

# Returns the version
def get_version():
    """ Gets the version from the package's __init__ file
    if there is some problem, let it happily fail """

    try:
        VERSIONFILE = os.path.join(here, "src", PACKAGE, "__init__.py")
        initfile_lines = open(VERSIONFILE, "rt").readlines()
        VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
        for line in initfile_lines:
            mo = re.search(VSRE, line, re.M)
            if mo:
                return mo.group(1)
    except:
        return 'n/d'

# load long description from README

with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name=PACKAGE,
    version=get_version(),
    description="Find your Italian Fiscal Code",
    author="A. Sala",
    author_email="andrea.sala98@gmail.com",
    url="https://github.com/andreasala98/getmycf",
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={"": ["data/*.csv"]},
    entry_points={'console_scripts': ['getcf = getcf.main:main',
                                     'getcf-reverse = getcf.main:reverse']},
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
        "Natural Language :: Italian"
    ],
    install_requires=[
        "numpy",
        "pytest"
    ],
    python_requires=">=3.7.0",
    long_description=long_description,
    long_description_content_type='text/markdown',
)

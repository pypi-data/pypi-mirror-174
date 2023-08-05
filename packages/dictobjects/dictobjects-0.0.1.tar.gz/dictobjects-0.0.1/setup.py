from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.0.1'
DESCRIPTION = 'Convert dictionaries to objects '
LONG_DESCRIPTION = 'A package that converts a dictionaries to python objects with the keys as attributes.'

# Setting up
setup(
    name="dictobjects",
    version=VERSION,
    author="DimJimm",
    author_email="<appleneticyt@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['simpledata'],
    keywords=['python', 'dict', 'dictionary', 'obj', 'objects', 'object', 'dictionaries', 'dicts', 'convert', 'conversion', 'attributes', 'keys', 'values'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
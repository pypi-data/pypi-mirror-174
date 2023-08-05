from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.0.1'
DESCRIPTION = 'Load and write json and pickle files or strings, the simple way.'
LONG_DESCRIPTION = 'A package that makes the reading, writing, creating and parsing of files/strings very simple and straightforward'

# Setting up
setup(
    name='simpledata',
    version=VERSION,
    author='DimJimm',
    author_email='<appleneticyt@gmail.com>',
    description=DESCRIPTION,
    long_description_content_type='text/markdown',
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'files', 'file', 'io', 'json', 'pickle', 'data', 'load', 'parse', 'create', 'write', 'simple', 'easy', 'straightforward', 'fs', 'filesystem'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: Unix',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
    ]
)
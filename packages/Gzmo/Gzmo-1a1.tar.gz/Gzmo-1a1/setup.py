# Standard library imports.
import os

# Setuptools package imports.
from setuptools import setup

# Read the README.rst file for the 'long_description' argument given
# to the setup function.
README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# Allow setup.py to be run from any path.
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name = 'Gzmo',
    version = '1a1',
    py_modules = ['gzmo'],
    entry_points = {'console_scripts': ['gzmo = gzmo:main']},
    license = 'BSD License',
    description = 'Process JSON like data structures using process strings',
    long_description = README,
    url = 'https://bitbucket.org/notequal/gzmo/',
    author = 'Stanley Engle',
    author_email = 'stan.engle@gmail.com',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.10'],)

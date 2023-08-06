
from setuptools import setup, find_packages
import os

VERSION = '0.0.1.2'
DESCRIPTION = 'The Ultimate Archie CLI'

def get_long_description():
    with open(os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf8",) as fp:
        return fp.read()
    
# Setting up
setup(
    name="archimedean",
    version=VERSION,
    author="Daniel Li",
    author_email="daniel.miami2005@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=get_long_description(),
    packages=find_packages(),
    install_requires=['requests', 'bs4', 'click'],
    keywords=['python', 'archimedean', 'archie',
              'archimedean upper conservatory', 'cinemath', 'automate archie'],
    python_requires='>=3.6'
)

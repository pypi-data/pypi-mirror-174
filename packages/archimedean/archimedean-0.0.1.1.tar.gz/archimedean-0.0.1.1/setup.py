
from setuptools import setup, find_packages

VERSION = '0.0.1.1'
DESCRIPTION = 'The Ultimate Archie CLI'
LONG_DESCRIPTION = 'Sends email whenever there is new homework on Archie website. Can download all files from any class in CineMath. Can download any resource posted on Archie. '

# Setting up
setup(
    name="archimedean",
    version=VERSION,
    author="Daniel Li",
    author_email="daniel.miami2005@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests', 'bs4', 'click'],
    keywords=['python', 'archimedean', 'archie',
              'archimedean upper conservatory', 'cinemath', 'automate archie'],
    python_requires='>=3.6'
)

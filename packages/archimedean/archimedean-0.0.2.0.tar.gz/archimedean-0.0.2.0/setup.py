
from setuptools import setup, find_packages
import os

# Setting up
setup(
    name="archimedean",
    version='0.0.2.0',
    author="Daniel Li",
    author_email="daniel.miami2005@gmail.com",
    description='The Ultimate Archie CLI',
    long_description_content_type="text/markdown",
    long_description=open(os.path.join(os.path.dirname(
        __file__), "README.md")).read(),
    packages=find_packages(),
    install_requires=['requests', 'bs4', 'os', 'sys'],
    keywords=['python', 'archimedean', 'archie',
              'archimedean upper conservatory', 'cinemath', 'automate archie'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': ['archimedean = archie.archie:main']
    },
    python_requires='>=3.6'
)

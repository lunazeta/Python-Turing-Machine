from setuptools import setup

__project__ = "qwhatyTuring"
__desc__ = "Turing Machine in Python"
__version__ = "1.1.0"
__author__ = "qwhaty"
__author_email__ = "qwhaty@hotmail.com"
__license__ = "MIT"
__url__ = "https://github.com/qwhaty/Python-Turing-Machine"
__long_description__ = '''# Turing Machines in Python

Visit [the project page](https://github.com/qwhaty/Python-Turing-Machine) for more information

'''

__classifiers__ = [
    "Intended Audience :: Education",
    "Topic :: Education",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11"
]

setup(
    name=__project__,
    version=__version__,
    description=__desc__,
    long_description=__long_description__,
    url=__url__,
    author=__author__,
    author_email=__author_email__,
    license=__license__,
    packages=[__project__],
    classifiers=__classifiers__,
    install_requires=["pygame"]
)
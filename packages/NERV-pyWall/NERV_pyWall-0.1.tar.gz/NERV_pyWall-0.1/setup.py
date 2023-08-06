import setuptools
from setuptools import setup, find_packages

setup(
    name = "NERV_pyWall",
    version = "0.1",
    description = "First assignment",
    long_description = "NERV project for the first assignment",
    long_description_content_type = 'text/x-rst',
    url = "https://gitlab.com/nerv8/2022_assignment1_pywall.git",
    author = "NERV Team",
    license = "MIT",
    classifiers = [
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9'
    ],
    packages=find_packages("src"),
    python_requires = '>=3'
)

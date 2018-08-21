#!/usr/bin/env python

from deployfish_ext import __version__
from setuptools import setup, find_packages

setup(
    name="deployfish-ext",
    version=__version__,
    description="Deployfish Cnyes extend plugin",
    author="Cnyes Backend Team",
    author_email="rd-backend@cnyes.com",
    url="https://bitbucket.org/cnyesrd/deployfish-ext",
    keywords=['aws', 'ecs', 'docker', 'devops'],
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3"
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click >= 6.7", "deployfish >= 0.24.0", "boto3 >= 1.7.55", "botocore >= 1.10.55"
    ],
    entry_points={'deployfish.command.plugins': ['ext = deployfish_ext.cli']},
)

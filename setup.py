#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

if "__main__" == __name__:
    setup(
        author="Hao-Ting Wang",
        author_email='htwangtw@gmail.com',
        python_requires='>=3.7',
        description="BIDS dataset on AWS to datalad",
        name='buildnki',
        packages=find_packages(),
        version='0.0.1',
        install_requires=['boto', 'click'],
        entry_points='''
        [console_scripts]
        s3crawler=buildnki.cli:main
    ''',
    )
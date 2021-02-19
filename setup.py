#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

if "__main__" == __name__:
    setup(
        author="Hao-Ting Wang",
        author_email='htwangtw@gmail.com',
        python_requires='>=3.7',
        description="Crawl public BIDS dataset on AWS to datalad",
        name='publiccrawler',
        packages=find_packages(),
        version='0.0.1',
        install_requires=['boto', 'click'],
        entry_points='''
        [console_scripts]
        s3crawler=publiccrawler.cli:main
    ''',
    )
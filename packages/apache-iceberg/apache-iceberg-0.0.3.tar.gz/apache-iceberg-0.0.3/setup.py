from setuptools import setup, find_packages
from setuptools.command.install import install

import os

class post_install(install):
    def run(self):
        raise RuntimeError('Please install pyiceberg instead')

setup(
    name='apache-iceberg',
    version='0.0.3',
    url='https://github.com/apache/iceberg',
    author='Apache Software Foundation',
    author_email='dev@iceberg.apache.org',
    description='Iceberg is a high-performance format for huge analytic tables.',
    packages=find_packages(),
    install_requires=[],
    cmdclass={'install': post_install},
)

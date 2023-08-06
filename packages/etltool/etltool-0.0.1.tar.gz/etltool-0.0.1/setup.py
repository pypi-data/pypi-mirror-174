# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(name='etltool',
      version='0.0.1',
      description='etl tool',
      author='yangsong',
      author_email='yangsong@hinterstellar.com',
      requires=['gzip', 'shutil', 'boto3', 'json', 'codesc', 'pymongo', 'bson'],
      packages=find_packages(),
      license='apache 3.0')
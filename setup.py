#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='Avro-SQS Anomaly Reporter',
      version='0.2',
      description='Avro-Based SQS forwarder for Anomalies',
      author='Jason Bau',
      author_email='jasonbau@gmail.com',
      packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
      license='LICENSE.txt',
      install_requires=[
          'boto3>=1.9.59', 'avro>=1.8.2'
      ]
)

#!/usr/bin/env python

from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(name='erp_utils',
      version='0.1.132',
      description='This package contains modules shared between erp microservices',
      author='Antoine Wood',
      author_email='antoine@thefurnitureguys.ca',
      packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
      install_requires=[
          'setuptools',
          'djangorestframework',
          'requests',
          'boto3',
          'django',
          'botocore',
          'beautifulsoup4',
          'environ',
          'faker',
          'django-auto-prefetching',
          'botocore',
          'reportlab==3.6.6',
          'xhtml2pdf'

      ],
      )

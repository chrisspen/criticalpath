#!/usr/bin/env python

from os import path
from setuptools import setup, find_packages

import criticalpath

with open(path.join(path.abspath(path.dirname(__file__)), 'README.md')) as f:
    long_description = f.read()

setup(
    name='criticalpath',
    version=criticalpath.__version__,
    packages=find_packages(),
    package_data={
        'criticalpath': [
            'fixtures/*',
        ],
    },
    author='Chris Spencer',
    author_email='chrisspen@gmail.com',
    description='Calculates the critical path in a task network.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='LGPL',
    url='https://github.com/chrisspen/criticalpath',
    #https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6'
    ],
    zip_safe=False,
)

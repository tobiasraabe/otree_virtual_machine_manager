#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click >= 6.0',
    'psycopg2 >= 2.6.2',
    'plumbum >= 1.6.3',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='ovmm',
    version='0.1.0',
    description="oTree Virtual Machine Manager helps to manage user accounts.",
    long_description=readme + '\n\n' + history,
    author='Tobias Raabe',
    author_email='tobiasraabe@uni-bonn.de',
    url='https://github.com/tobiasraabe/ovmm',
    packages=[
        'ovmm',
        'ovmm.commands',
        'ovmm.handlers',
        'ovmm.prompts',
        'ovmm.templates',
    ],
    package_dir={'ovmm':
                 'ovmm'},
    entry_points={
        'console_scripts': [
            # 'ovmm=ovmm.cli:main',
            'ovmm=ovmm.cli:cli'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license='MIT license',
    zip_safe=False,
    keywords='ovmm',
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
        'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive'
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements
)

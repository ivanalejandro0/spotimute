#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from buildqt import BuildQt

cmdclass = {}
cmdclass['build_qt'] = BuildQt

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = [
    # TODO: put package requirements here
    'PySide',
    'sh',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='spotimute',
    version='0.1.0',
    description="Mute the Spotify songs you don't like",
    long_description=readme + '\n\n' + history,
    author='Ivan Alejandro',
    author_email='ivanalejandro0@gmail.com',
    url='https://github.com/ivanalejandro0/spotimute',
    packages=[
        'spotimute',
    ],
    package_dir={'spotimute':
                 'spotimute'},
    include_package_data=True,
    install_requires=requirements,
    license="GPLv2",
    zip_safe=False,
    keywords='Spotify, mute, muter, songs',
    cmdclass=cmdclass,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
    tests_require=test_requirements
)

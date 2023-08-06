#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

test_requirements = [ ]

setup(
    author="Rasmus Eklund",
    author_email='rasmus.eklund@psychology.su.se',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Tools for processing EEG data with MNE.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='raek_mne',
    name='raek_mne',
    packages=find_packages(include=['raek_mne', 'raek_mne.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/Eklund89/raek_mne',
    version='2022.11.01',
    zip_safe=False,
)

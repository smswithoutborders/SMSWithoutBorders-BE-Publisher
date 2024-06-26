"""
SwobBackendPublisher Setup Script
"""

import os
from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    readme = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [req.strip() for req in fh.readlines()]

setup(
    name='SwobBackendPublisher',
    packages=find_packages(),
    version='0.1.0',
    description='SMSWithoutBorders Backend Publisher library',
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/smswithoutborders/SMSWithoutBorders-BE-Publisher",
    author='Afkanerd',
    author_email='developers@smswithoutborders.com',
    license="GPLv3",
    install_requires=requirements,
    test_suite='tests',
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
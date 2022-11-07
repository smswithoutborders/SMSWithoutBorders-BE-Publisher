import os
from setuptools import find_packages, setup
from SwobBackendPublisher import __version__
from SwobBackendPublisher import __author__
from SwobBackendPublisher import __license__

f = open(os.path.join(os.path.dirname(__file__), 'README.md'))
readme = f.read()
f.close()

setup(
    name='SwobBackendPublisher',
    packages=find_packages(include=['SwobBackendPublisher']),
    version=__version__,
    description='SMSWithoutBorders Backend Publisher library',
    long_description=readme,
    author=__author__,
    author_email='developers@smswithoutborders.com',
    license=__license__,
    install_requires=[
        'mysql-connector-python==8.0.29',
        'mysqlclient==2.1.1',
        'peewee==3.15.1',
        'protobuf==4.21.9',
        'pycryptodome==3.14.1',
        'Werkzeug==2.1.2'
    ],
    test_suite='tests',
)
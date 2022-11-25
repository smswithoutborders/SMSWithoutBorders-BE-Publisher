import os
from setuptools import find_packages, setup

f = open(os.path.join(os.path.dirname(__file__), 'README.md'))
readme = f.read()
f.close()

setup(
    name='SwobBackendPublisher',
    packages=find_packages(),
    version='0.1.0',
    description='SMSWithoutBorders Backend Publisher library',
    long_description=readme,
    author='Afkanerd',
    author_email='developers@smswithoutborders.com',
    license='The GNU General Public License v3.0',
    install_requires=[
        'mysql-connector-python==8.0.29',
        'mysqlclient==2.1.1',
        'peewee==3.15.1',
        'protobuf==4.21.9',
        'pycryptodome==3.14.1',
        'SwobThirdPartyPlatforms @ git+https://github.com/smswithoutborders/SMSWithoutBorders-Customized-Third-Party-Platforms.git@main#egg=SwobThirdPartyPlatforms'
    ],
    test_suite='tests',
)
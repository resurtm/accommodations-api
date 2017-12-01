#!/usr/bin/env python3

from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='accommodations-api',
    packages=['accommodations'],
    version='0.0.1',
    description='Accommodations API',
    long_description=readme(),
    url='https://github.com/resurtm/accommodations-api',
    download_url='https://github.com/resurtm/accommodations-api/archive/v0.0.1.tar.gz',
    author='resurtm',
    author_email='resurtm@gmail.com',
    license='MIT',
    classifiers=[],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask',
        'Flask-PyMongo',
        'celery',
        'jsonschema',
        'bcrypt',
        'PyJWT',
        'python-slugify',
        'bson',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)

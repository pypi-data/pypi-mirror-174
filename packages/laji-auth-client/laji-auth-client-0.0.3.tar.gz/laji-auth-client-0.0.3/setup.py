from setuptools import setup, find_packages
import os

VERSION = '0.0.3'
DESCRIPTION = 'Python client for Laji-auth'


def get_long_description():
    with open(
        os.path.join(os.path.dirname(__file__), 'README.md'),
        encoding='utf8',
    ) as fp:
        return fp.read()


setup(
    name='laji-auth-client',
    version=VERSION,
    author='Meeri Rannisto',
    author_email='meeri.rannisto@helsinki.fi',
    description=DESCRIPTION,
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/luomus/laji-auth-client-python',
    license='MIT',
    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=['requests']
)

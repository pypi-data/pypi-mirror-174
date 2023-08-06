from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'Python client for Laji-auth'

setup(
    name='laji-auth-client',
    version=VERSION,
    author='Meeri Rannisto',
    author_email='meeri.rannisto@helsinki.fi',
    description=DESCRIPTION,
    license_files=['LICENSE'],
    packages=find_packages(),
    install_requires=['requests']
)

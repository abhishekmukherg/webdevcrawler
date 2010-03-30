import distribute_setup
distribute_setup.use_setuptools()

from setuptools import setup, find_packages

setup(
    name='webcrawler',
    version='0.1',
    author='Abhishek Mukherjee',
    author_email='abhishek.mukher.g@gmail.com',

    packages=['webcrawler'],
    test_suite='tests',
    install_requires=[
        'storm',
    ],
)

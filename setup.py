from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

setup(
        name="webdevcrawler",
        version="0.1",
        install_requires=[
            'django',
            'distribute',
            'django_cas',
            'BeautifulSoup',
        ],
        extras_require={
            'evolve': ['django-evolution'],
            'debug': ['django-debug-toolbar'],
        },
        packages = find_packages('src'),
        package_dir = {'': 'src'},

        )

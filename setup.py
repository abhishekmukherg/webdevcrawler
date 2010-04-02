from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

setup(
      name="webdevcrawler",
      version="0.1",
      install_requires=[
          'django',
          'distribute',
      ],
      packages = find_packages('src'),
      package_dir = {'': 'src'},

)

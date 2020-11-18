
from setuptools import find_packages, setup

setup(
    name='pyredpocket',
    url='https://github.com/ronnie-llamado/redpocket-monitor',
    author='Ronnie Llamado',
    packages=find_packages( exclude=( 'tests', ) ),
)

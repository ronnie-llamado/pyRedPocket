
import re
from setuptools import find_packages
from setuptools import setup

def find_version():
    with open('redpocket_monitor/__init__.py') as fp:
        for line in fp:
            # __version__ = '0.1.0'
            match = re.search(r"__version__\s*=\s*'([^']+)'", line)
            if match:
                return match.group(1)
    assert False, 'cannot find version'

setup(
    name='redpocket-monitor',
    version=find_version(),
    url='https://github.com/ronnie-llamado/redpocket-monitor',
    author='Ronnie Llamado',
    packages=find_packages( exclude=( 'tests', ) )
)

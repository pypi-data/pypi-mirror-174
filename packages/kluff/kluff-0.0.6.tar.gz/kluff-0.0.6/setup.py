
from setuptools import setup, find_packages
from kluff.core.version import get_version

VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='kluff',
    version=VERSION,
    description='Build and Deploy with Kluff',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Vinay Gode',
    author_email='vinay@kluff.com',
    url='https://github.com/kluff-com/kluff-cli',
    license='unlicensed',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={'kluff': ['templates/*']},
    include_package_data=True,
    entry_points="""
        [console_scripts]
        kluff = kluff.main:main
    """,
)

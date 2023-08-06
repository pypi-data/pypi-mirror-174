from setuptools import setup,find_packages
from os import  path

here=path.abspath(path.dirname(__file__))

setup(
    name='my_00077',
    version='0.1',
    author='krisss',
    author_email='kris@ex.ex',
    packages=find_packages(),
    include_package_data=True,
    description='Super usefull piece',
    install_requires=['names'],
    scripts=['my_names2/my_names2.py','bin/gen_names.bat']
)


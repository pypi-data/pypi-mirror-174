# -*- coding:utf-8 -*-
from distutils.core import setup
import setuptools
packages = ['papeete']
setup(name='papeete',
	version='1.01',
	author='md_soft',
    packages=packages, 
    package_dir={'requests': 'requests'},)
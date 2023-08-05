from distutils.core import  setup
import setuptools
packages = ['Test-Pypi-GYW']# 唯一的包名，自己取名
setup(name='Test-Pypi-GYW',
	version='1.2',
	author='guanyuwei',
    packages=packages,
    package_dir={'requests': 'requests'},)





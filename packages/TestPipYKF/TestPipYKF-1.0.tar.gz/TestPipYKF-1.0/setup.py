from distutils.core import  setup
import setuptools
packages = ['TestPipYKF']# 唯一的包名，自己取名
setup(name='TestPipYKF',
	version='1.0',
	author='guanyuwei',
    packages=packages,
    package_dir={'requests': 'requests'},)





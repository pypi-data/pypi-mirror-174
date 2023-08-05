
from setuptools import setup, find_packages



packages = ["Test-Pypi-GYW"]# 唯一的包名，自己取名
setup(name='Test-Pypi-GYW', # 打包后的文件名
	  version='1.1',  # 版本号
      description='A package to test',
	  author='gyw',
      include_package_data = True, # 包含项目中的静态资源
      package_dir={'requests': 'requests'},
      license="apache 3.0",
      packages = find_packages(),  # 默认在与 setup.py 文件同一目录下搜索各个含有 __init__.py 的目录做为要添加的包
      )




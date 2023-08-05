from distutils.core import  setup
from setuptools import setup, find_packages
import setuptools


packages = ["RealtimeMouseDetect"]# 唯一的包名，自己取名
setup(name='RealtimeMouseDetect', # 打包后的文件名
	  version='1.2',  # 版本号
      description='A package to detect what you said without voice just by reading your lips in realtime',
	  author='gyw',
      include_package_data = True, # 包含项目中的静态资源
      package_dir={'requests': 'requests'},
      license="apache 3.0",
      packages = find_packages(),  # 默认在与 setup.py 文件同一目录下搜索各个含有 __init__.py 的目录做为要添加的包
      )




from distutils.core import setup
from setuptools import find_packages
# python setup.py bdist_wheel # 打包为whl文件
# python setup.py sdist # 打包为tar.gz文件
#twine upload dist/*
#qq

setup(name='stduino',  # 包名
      version='0.1.10',  # 版本号
      description='Stduino IDE For win、mac、linux',
      long_description='Stduino IDE For Embedded development.',
      author='文涛',
      author_email='33672008@qq.com',
      url='http://www.stduino.com',
      license='',#'pyqtwebengine>=5.15',
      install_requires=['click==7.1.2','pyserial>=2.0','pyqt5==5.13.0','pywebview>=3.0','requests>=2.20','qdarkstyle==2.8.1','pygdbmi>=0.10','qscintilla==2.11.2','watchdog>=2.1'],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Topic :: Utilities'
      ],
      keywords='Stduino IDE',
      packages=find_packages('src'),  # 必填，就是包的代码主目录
      package_dir={'': 'src'},  # 必填
      include_package_data=True,
      )

import codecs
import os
import sys
try:
    from setuptools import setup
except:
    from distutils.core import setup

"""
打包的用的setup必须引入，

"""
def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()

NAME = "welog"  # 1，需要改：模块名

PACKAGES = ["welog", ]  # 2，需要改：模块名

DESCRIPTION = "this is a welog package for collect log infomation from distribution container environment to filebeat center."


LONG_DESCRIPTION = read("README.rst")

KEYWORDS = "welog"  # 关键字，可选改

AUTHOR = "Wei Wei"  # 3，需要改：作者名

AUTHOR_EMAIL = "w.w@taoxiang.org"  # 4，需要改：邮箱

URL = "http://www.python.org"  # 5，需要改：一般写模块的github地址

VERSION = "1.1.6"  # 6，需要改：版本号

LICENSE = "MIT"  # 授权方式，可选改


setup(
    name = NAME,
    version = VERSION,
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    keywords = KEYWORDS,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    url = URL,
    license = LICENSE,
    packages = PACKAGES,
    include_package_data = True,
    zip_safe = True,
)

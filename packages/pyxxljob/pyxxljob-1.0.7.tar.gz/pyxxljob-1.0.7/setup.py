import codecs
import os
import sys
try:
    from setuptools import setup
except:
    from distutils.core import setup

CUR_DIR = os.path.abspath(os.path.dirname(__file__))
README = os.path.join(CUR_DIR, "README.md")
with open("README.md", "r") as fd:
    long_description = fd.read()

NAME = "pyxxljob"
PACKAGES = ['pyxxljob']
DESCRIPTION = "A Python executor for XXL-jobs"
KEYWORDS = "xxljob"
AUTHOR = "bingbing.tu"
AUTHOR_EMAIL = "2917073217@qq.com"
URL = "https://github.com/fcfangcc/pyxxl"
VERSION = "1.0.7"
LICENSE = "MIT"
setup(
    name =NAME,version = VERSION,
    description = DESCRIPTION,
    #long_description=long_description,
    classifiers =[
         "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords =KEYWORDS,author = AUTHOR,
    author_email = AUTHOR_EMAIL,url = URL,
    packages = PACKAGES,include_package_data=True,zip_safe=True,
    entry_points={
      },

)
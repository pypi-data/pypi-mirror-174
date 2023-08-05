from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'CoolDevcode Version 0.0.1'
# Setting up
setup(
    name="cooldevcode",
    version=VERSION,
    author="YeaeThawe",
    author_email="<yeaethawe@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['tkinter', 'string'],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

from __future__ import print_function
from setuptools import setup, find_packages
import sys

setup(
    name="vionic_pack",
    version="0.1.0",
    author="vionic",  
    author_email="1356617750@qq.com",
    description="A dash for jupyter test.",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Environment :: Web Environment",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: Microsoft',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.8',
    ],
    install_requires=[
            'pandas>=1.5.1',  #所需要包的版本号
            'numpy>=1.23.4'   #所需要包的版本号
    ],
    zip_safe=True,
)

#!/usr/bin/env python

from io import open
from setuptools import setup, find_packages


"""
:authors: Superior_6564
:license: Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2022 Superior_6564
"""


# with open('README.md') as f:
#     previous_version = f.readline()[22:].strip()
#     if int(previous_version[4]) < 9:
#         previous_num = previous_version[4]
#         new_num = str(int(previous_version[4]) + 1)
#         new_version = previous_version[:-1] + new_num
#     elif int(previous_version[2]) < 9:
#         previous_num = previous_version[2]
#         new_num = str(int(previous_version[2]) + 1)
#         new_version = previous_version[0:2] + new_num + ".0"
#     elif int(previous_version[0]) < 9:
#         previous_num = previous_version[0]
#         new_num = str(int(previous_version[0]) + 1)
#         new_version = new_num + "0.0"
#     test_description = f.read()
# version = new_version

version = '0.3.3'
# 0.1.9

with open('README.md') as f:
    line_dict = {"Theme": f.readline(), "Space_1": f.readline(), "Name": f.readline(),
                 "Space_2": f.readline(), "Version": f.readline()[:9], "Everything_else": f.read()}

with open('README.md', "w") as f:
    write_readme = line_dict["Theme"] + line_dict["Space_1"] + line_dict["Name"] + \
                   line_dict["Space_2"] + line_dict["Version"] + version + "\n" + line_dict["Everything_else"]
    f.write(write_readme)

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='superior6564',
    version=version,

    author='Superior_6564',
    author_email='vip.klochayil@gmail.com',

    description=(
        u'Before using you need to run: from superior6564 import required_pack; required_pack.install()'
    ),
    long_description=long_description,
    # long_description_content_type='text/markdown',

    url='https://github.com/Superior-GitHub/Superior6564',
    download_url='https://github.com/Superior-GitHub/Superior6564/archive/refs/heads/main.zip'.format(version),

    license='Apache License, Version 2.0, see LICENSE file',

    packages=find_packages(),
    install_requires=['', ''],

    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ]
)

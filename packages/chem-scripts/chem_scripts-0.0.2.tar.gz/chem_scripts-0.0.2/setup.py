#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/7/4 14:56
# @Author  : zbc@mail.ustc.edu.cn
# @File    : setup.py
# @Software: PyCharm

from setuptools import setup

with open('README.md', 'r', encoding='utf-8')as f:
    long_description = f.read()

setup(
    name='chem_scripts',
    version='0.0.2',
    author='zbc',
    author_email='zbc@mail.ustc.edu.cn',
    url='https://github.com/zbc0315/chem_scripts',
    description=u'chemical scripts',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['chem_scripts', 'chem_scripts/rxn_template', 'chem_scripts/chem_handler',
              'chem_scripts/mol_handler', 'chem_scripts/rxn_handler'],
    install_requires=['rdkit'],
    include_package_data=True,
    entry_points={
        'console_scripts': [

        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6'
)


if __name__ == "__main__":
    pass

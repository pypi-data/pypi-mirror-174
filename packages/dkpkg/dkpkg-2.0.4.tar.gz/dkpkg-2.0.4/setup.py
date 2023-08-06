#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""dkpkg - standardized package structure names
"""

classifiers = """\
Development Status :: 3 - Alpha
Intended Audience :: Developers
Natural Language :: English
License :: OSI Approved :: BSD License
Operating System :: OS Independent
Programming Language :: Python
Programming Language :: Python :: 3
Topic :: Software Development :: Libraries
"""

import setuptools

version = '2.0.4'


setuptools.setup(
    name='dkpkg',
    version=version,
    install_requires=[
        'invoke',
        'PyYAML',
        'dkfileutils',
        'dk-tasklib',
        'yamldirs',
    ],
    author='Bjorn Pettersen',
    author_email='bp@datakortet.no',
    url='https://github.com/datakortet/dkpkg',
    license='BSD',
    description=__doc__.strip(),
    classifiers=[line for line in classifiers.split('\n') if line],
    long_description=open('README.rst').read(),
    packages=setuptools.find_packages(),
    zip_safe=False,
)

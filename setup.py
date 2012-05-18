#!/usr/bin/env python
from distutils.core import setup
from checklistdsl.version import get_version

setup(
    name='ChecklistDSL',
    version=get_version(),
    description='A simple markup DSL for creating checklists.',
    long_description=open('README.rst').read(),
    author='Nicholas H.Tollervey',
    author_email='ntoll@ntoll.org',
    url='http://packages.python.org/checklistdsl',
    packages=['checklistdsl'],
    license='MIT',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Topic :: Communications',
        'Topic :: Database',
        'Topic :: Internet',
    ]
)

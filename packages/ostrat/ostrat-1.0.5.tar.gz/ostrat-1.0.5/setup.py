#!/usr/bin/env python

from io import open
from setuptools import setup

"""
:authors: lexek
:license: OSI Approved :: GNU General Public License v3 (GPLv3)
:copyright: (c) 2022 lexek
"""

version = '1.0.5'

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ostrat',
    version=version,

    author='lexek',
    author_email='minelanpro@gmail.ru',

    description=(
        u'Open-Source Telegram Remote Administration Tool - Remote PC access via Telegram Bot.'
    ),
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://sourceforge.net/projects/ostrat/',
    download_url='https://sourceforge.net/projects/ostrat/files/ostRAT/',

    license='OSI Approved :: GNU General Public License v3 (GPLv3)',

    packages=['ostrat'],
    install_requires=['requests', 'opencv-python', 'aiogram', 'keyboard', 'mouse', 'bs4', 'pillow', 'colorama'],

    classifiers=[
        
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: Microsoft :: Windows',
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Topic :: System :: Systems Administration',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.10',
        
    ]
)

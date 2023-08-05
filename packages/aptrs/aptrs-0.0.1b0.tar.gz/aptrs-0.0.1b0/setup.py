#!/usr/bin/env python3

from setuptools import (
    find_packages,
    setup,
)

from pathlib import Path


def read(rel_path):
    init = Path(__file__).resolve().parent / rel_path
    return init.read_text('utf-8', 'ignore')



description = (
    'Automated Penetration Testing Reporting System')

setup(
    name='aptrs',
    version='0.0.1b',
    description=description,
    author='AnoF',
    author_email='kalalsourav20@gmail.com',
    packages=find_packages(include=[
        '*', 'aptrs.*',
    ]),
    include_package_data=True,
    python_requires='>=3.8+',
    entry_points={
        'console_scripts': [
            'aptrs = APTRS.__main__:main',
        ],
    },
    url='https://github.com/Anof-cyber/APTRS',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    install_requires=Path('requirements.txt').read_text().splitlines(),
)
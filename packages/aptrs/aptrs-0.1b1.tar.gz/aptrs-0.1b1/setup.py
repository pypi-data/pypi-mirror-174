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
    version='0.1b1',
    description=description,
    author='AnoF',
    author_email='kalalsourav20@gmail.com',
    packages=find_packages(include=[
        'aptrs', 'aptrs.*',
    ]),
    include_package_data=True,
    python_requires='>=3.8+',
    entry_points={
        'console_scripts': [
            'aptrs = aptrs.__main__:main',
        ],
    },
    url='https://github.com/Anof-cyber/APTRS',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    install_requires=['asgiref==3.5.2', 'backports.zoneinfo==0.2.1', 'Django==4.1.2', 'django-ckeditor==6.5.1', 'django-js-asset==2.0.0', 'django-pdfkit==0.3.1', 'django-phonenumber-field==7.0.0', 'django-phonenumbers==1.0.1', 'gunicorn==20.1.0', 'pdfkit==0.6.0', 'phonenumbers==8.12.57', 'Pillow==9.2.0', 'PyPDF2==2.11.1', 'sqlparse==0.4.3', 'typing-extensions==4.4.0', 'tzdata==2022.5', 'waitress==2.1.2'],
)
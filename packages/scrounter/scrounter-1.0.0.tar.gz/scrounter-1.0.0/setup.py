#!/usr/bin/env python3

from setuptools import setup, find_packages

version = '1.0.0'

setup(
    name='scrounter',
    version=version,
    author='Blackoutseeker (Felipe Pereira)',
    author_email='felipsdev@gmail.com',
    url='https://github.com/Blackoutseeker/Felips-Counter-Python',
    packages=find_packages(exclude='tests'),
    python_requires='>=3.7',
    description='Count your project lines easily!',
    long_description='Count your project lines easily!',
    long_description_content_type='text/markdown',
    keywords=['felips', 'counter'],
    entry_points={
        'console_scripts': [
            'felips_counter=scrounter.__main__:main'
        ]
    }
)

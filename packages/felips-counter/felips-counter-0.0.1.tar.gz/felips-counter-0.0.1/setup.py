#!/usr/bin/env python3

from setuptools import setup, find_packages

if __name__ == '__main__':
    with open('README.md', 'r') as readme:
        long_description = readme.read()

    setup(
        name='felips-counter',
        version='0.0.1',
        author='Blackoutseeker (Felipe Pereira)',
        author_email='felipsdev@gmail.com',
        url='https://github.com/Blackoutseeker/Felips-Counter-Python',
        packages=find_packages(exclude='tests'),
        python_requires='>=3.7',
        description='Count your project lines easily!',
        long_description=long_description,
        long_description_content_type='text/markdown',
        keywords=['felips', 'counter'],
        entry_points={
            'console_scripts': [
                'counter=felips_counter.__main__:main'
            ]
        }
    )

from setuptools import setup, find_packages
from pathlib import Path

setup(
    name='Pydf',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'xlsx2csv==0.8.2',
        'Markdown==3.4.1',
    ],
    extras_require={
        'numpy': ['numpy'],
    },
    author='Ray Lutz',
    author_email='raylutz@cognisys.com',
    description='Python Daffodil (Pydf) provides lightweight and fast 2-D dataframes',
    long_description=Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    url='https://github.com/raylutz/Pydf',
    python_requires='>=3.6',
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

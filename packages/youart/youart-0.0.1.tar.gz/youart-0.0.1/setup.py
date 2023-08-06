#!/usr/bin/env python3
# coding: utf-8

from setuptools import setup

# package information (is filling from youart/release.py)
__version__ = ''
__author__ = ''
__contact__ = ''
__url__ = ''
__license__ = ''


# Get the information from youart/release.py without importing the package
exec(compile(open('youart/release.py').read(),
             'youart/release.py', 'exec'))

with open("README.md", encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='youart',
    version=__version__,
    description='monitor and save UART logs',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=__url__,
    author=__author__,
    author_email=__contact__,
    license=__license__,
    packages=['youart'],
    entry_points={
        'console_scripts': ['youart=youart.cli:main'],
    },
    install_requires=[
        'pyserial',
    ],
    python_requires='>=3.7',
    zip_safe=False,
    keywords='UART serial',
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3 :: Only',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Topic :: Utilities'
    ],
    project_urls={
        'source': __url__
    }
)

#!/usr/bin/env python

from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='Flask-Hmin',
    version='1.0.0',
    url='https://github.com/zhenzi0322/Flask-Hmin',
    license='MIT',
    author='玉振',
    author_email='82131529@qq.com',
    description="Flask压缩Html",
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules=['HMIN'],
    packages=['flask_hmin'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'htmlmin'
    ],
    python_requires='>=3.6',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Markup :: HTML',
    ],
)
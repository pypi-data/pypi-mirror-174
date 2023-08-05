import re

from setuptools import setup, find_packages


def read(path):
    with open(path, 'r', encoding='utf8') as fp:
        content = fp.read()
    return content


def find_version(path):
    match = re.search(r'__version__ = [\'"](?P<version>[^\'"]*)[\'"]', read(path))
    if match:
        return match.group('version')
    raise RuntimeError("Cannot find version information")


setup(
    name='bums',
    version=find_version('bums/version.py'),
    author='cheer',
    author_email='cheerxiong0823@163.com',
    description='好用的Python函数集合',
    long_description='README.md',
    url='https://gitee.com/cheerxiong/bums',
    packages=find_packages(),
    python_requires=">=3.6",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)

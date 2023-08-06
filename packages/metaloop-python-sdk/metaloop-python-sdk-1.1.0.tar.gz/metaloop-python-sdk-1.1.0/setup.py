from setuptools import find_packages, setup
import os

ROOT = os.path.dirname(__file__)


def get_version():
    version = open(os.path.join(ROOT, 'VERSION.txt')).read()
    return version


def get_requires():
    with open(os.path.join(ROOT, 'requirements.txt'), "r") as f:
        lines = f.readlines()
    return [x.strip() for x in lines]


setup(
    name='metaloop-python-sdk',
    version=get_version(),
    packages=find_packages(exclude=['tests*']),
    url='http://data.deepglint.com/',
    license='Apache License 2.0',
    author='yuma',
    author_email='yuma@deepglint.com',
    description='Deepglint Metaloop Python SDK',
    long_description_content_type='text/markdown',
    long_description=open('README.md', encoding='utf-8').read(),
    python_requires=">= 3.7",
    install_requires=get_requires(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    project_urls={
        'Documentation': 'https://gitlab.deepglint.com/metaloop/metaloop-python-sdk',
        'Source': 'https://gitlab.deepglint.com/metaloop/metaloop-python-sdk',
    },
)

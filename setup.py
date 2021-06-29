from setuptools import setup, find_packages

setup(
    name="tweetpie",
    version='1.0',
    description='twitter helper scripts for marketing purpose',
    author='hakuna',
    url='https://github.com/query-me/tweetpie',
    packages=find_packages(),
    install_requires=open('requirements.txt').read().splitlines(),
)
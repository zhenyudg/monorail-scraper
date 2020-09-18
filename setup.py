from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='monorail_scraper',
    version='0.1.0',
    description='A tool to scrape and retrieve data from Monorail',
    long_description=readme,
    author='Zhen Yu Ding',
    author_email='go-file-an-issue@on-github.instead',
    url='https://github.com/zhenyudg/monorail-scraper',
    license=license,
    packages=find_packages(exclude=('tests',))
)

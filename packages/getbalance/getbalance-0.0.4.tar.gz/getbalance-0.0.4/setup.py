from setuptools import setup, find_packages

setup(
    name="getbalance",
    version='0.0.4',
    author="Norma Escobar",
    author_email="norma@normaescobar.com",
    description="A python library that provides a wallet address balance at any day.",
    long_description='''
## Introduction
getbalance is a Python library that provides a wallet address balance at any day.
It was born from the tedious task of manually adding/subracting values to get the balance of an address at any given day.
All kudos to the Ethereum team of developers for the free APIs.

## Security
By default getbalance does not guard against quadratic blowup or billion laughs xml attacks. To guard against these install defusedxml.

## Documentation
The documentation is at: https://krpbtc.com

* installation methods
* supported coins/tokens
* how to contribute
    
    ''',
    packages=find_packages(),
    long_description_content_type='text/markdown',
    install_requires=['openpyxl', 'requests']
)
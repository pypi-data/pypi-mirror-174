from setuptools import setup, find_packages

setup(
    name="verifytx",
    version='0.2.0',
    author="Norma Escobar",
    author_email="norma@normaescobar.com",
    description="A python library to verify blockchain confirmations and transactions integrated with Excel.",
    long_description='''
## Introduction
verifytx is a Python library to verify blockchain confirmations and transactions integrated with Excel.
It was born from a lack of existing libraries to verify on-chain transactions automatically and blazingly fast.
All kudos to the openpyxl team and library to read/write natively from Python the Office Open XML format.

## Security
By default verifytx does not guard against quadratic blowup or billion laughs xml attacks. To guard against these install defusedxml.

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
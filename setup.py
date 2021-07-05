
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="azspec",
    version="0.0.1",
    author="ahelal",
    description="Helper library to test Azure resources",
    long_description=long_description,
    url="https://github.com/ahlal/azspec",
    packages=['azspec'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
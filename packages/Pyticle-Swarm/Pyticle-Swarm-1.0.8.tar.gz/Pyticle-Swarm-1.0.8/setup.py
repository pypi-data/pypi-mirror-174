
from setuptools import setup

from codecs import open
from os import path

HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="Pyticle-Swarm",
    version="1.0.8",
    description="PSO library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pyticle-swarm.readthedocs.io/",
    author="Bruno Veiga, Ricardo Faia, Tiago Pinto, Zita Vale",
    author_email="btsve@isep.ipp.com, rfmfa@isep.ipp.pt, tcp@isep.ipp.pt, zav@isep.ipp.pt",
    license="BSD 3-Clause",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=["pyticleswarm"],
    include_package_data=True,
    install_requires=[
        "numpy==1.21.3",
        "matplotlib==3.4.3",
        "matplotlib-inline==0.1.3",
        "joblib==1.1.0"
    ]
)

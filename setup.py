from setuptools import setup

setup(
    name="DumpConverter",
    version="1.0.0",
    author="BP2014N1",
    author_email="BP2014N1@hpi.de",
    description=("Downloads and parses dumps of databases for "
                 "external validation in Wikidata extension WikidataQuality"),
    license="GNU GPL v2+",
    url="https://github.com/WikidataQuality/DumpConverter",
    packages=['dumpconverter'],
    install_requires=[
        "argparse==1.3.0",
        "lxml==3.4.2",
        "pytest==2.6.4",
        "tabulate==0.7.4",
        "testtools==1.7.1",
        "mock==1.0.1"
    ]
)
#!/usr/bin/env python

from setuptools import find_packages, setup

__author__ = [
    "Felix Nitsch",  # noqa
    "Christoph Schimeczek",  # noqa
    "Ulrich Frey",
    "Marc Deissenroth-Uhrig",  # noqa
    "Benjamin Fuchs",
    "A. Achraf El Ghazi",  # noqa
]
__copyright__ = "Copyright 2022, German Aerospace Center (DLR)"
__credits__ = ["Kristina Nienhaus", "Evelyn Sperber", "Seyedfarzad Sarfarazi"]  # noqa

__license__ = "Apache License 2.0"
__maintainer__ = "Felix Nitsch"  # noqa
__email__ = "fame@dlr.de"
__status__ = "Production"


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="fameio",
    version="1.6.1",
    description="Python scripts for operation of FAME models",
    long_description=readme(),
    long_description_content_type="text/markdown",
    keywords=["FAME", "agent-based modelling"],
    url="https://gitlab.com/fame-framework/fame-io/",
    author=", ".join(__author__),
    author_email=__email__,
    license=__license__,
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    entry_points={
        "console_scripts": [
            "makeFameRunConfig=fameio.scripts:makeFameRunConfig",
            "convertFameResults=fameio.scripts:convertFameResults",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "pandas",
        "fameprotobuf>=1.2,<1.3",  # noqa
        "pyyaml",
    ],
    extras_require={"test": ["pytest", "google.protobuf", "mockito"]},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.8",
)

from setuptools import setup, find_packages

VERSION = "0.0.4"
DESCRIPTION = "Kitbag with functions, metadata, plots etc. that are used within FCN and RTD"

setup(
    name="kitbag",
    version=VERSION,
    description=DESCRIPTION,
    packages=find_packages(),
)

""" Setup instructions for nt3irisadapter """
from setuptools import find_packages, setup

install_requires = ["pyyaml"]

setup(
    name="nt3irisadapter",
    description="IRIS Adapter for NovaTouch 3",
    author="novacom software GmbH",
    version="0.0.4",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=install_requires,
)

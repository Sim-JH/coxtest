from setuptools import find_packages, setup

setup(
    name="coxtest",
    description="coxtest module",
    author="sjh",
    version="0.1.0",
    packages=find_packages(include=['coxtest']),
    include_package_data=True,
)

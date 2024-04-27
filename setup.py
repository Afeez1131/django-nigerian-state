# setup.py
from setuptools import setup, find_packages

setup(
    name="django_nigerian_states",
    version="1.0",
    packages=find_packages(exclude=["tests"]),
    exclude_package_data={"": ["**/migrations/*"]},
)

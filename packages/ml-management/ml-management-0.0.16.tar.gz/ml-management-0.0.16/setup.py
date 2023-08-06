"""Setup for ml-management package."""
from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("VERSION", "r", encoding="utf-8") as f:
    version = f.read()

setup(
    name="ml-management",
    version=version,
    description="Python implementation of model pattern, dataset",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="ISPRAS MODIS",
    author_email="modis@ispras.ru",
    maintainer="Maxim Ryndin",
    packages=find_packages(include=["ML_management", "ML_management.*"]),
    include_package_data=True,
    # jsonschema 2.6.0 is the last one to support python 3.6
    install_requires=[
        "mlflow==1.21.0",
        "jsonschema==2.6.0",
        "requests_toolbelt==0.10.1",
    ],
    data_files=[("", ["VERSION"])],
    python_requires=">=3.6",
)

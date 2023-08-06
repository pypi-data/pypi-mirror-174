from setuptools import setup, find_packages
import codecs
import os

setup(
    name="sidetrekUtils",
    version="0.0.1",
    description="Sidetrek wrapper for MLflow",
    author="Nabil Ahmed",
    author_email="nabil@sidetrek.com",
    packages=find_packages(),
    install_requires=["mlflow", "boto3", "sidetrek-mlflow-plugin"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
    ]
)

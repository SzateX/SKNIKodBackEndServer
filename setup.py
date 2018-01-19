import os
from setuptools import setup, find_packages

setup(
    name="KoloRESTApi",
    version="0.0.1",
    author="SKNI KOD",
    author_email="jaksza18@gmail.com",
    description=("REST API for SKNI KOD Website"),
    install_requires=['django', 'djangorestframework', 'markdown', 'django-filter', 'django-oauth-toolkit'],
    license="MiT",
    keywords="www website etc",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MiT",
    ]
)
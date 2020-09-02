import os
from setuptools import setup, find_packages

setup(
    name="KoloRESTApi",
    version="0.0.1",
    author="SKNI KOD",
    author_email="jaksza18@gmail.com",
    description=("REST API for SKNI KOD Website"),
    install_requires=['django', 'djangorestframework', 'markdown',
                      'django-filter', 'django-oauth-toolkit',
                      'django-rest-auth', 'django-allauth',
                      'django-cors-headers',
                      'httpie', 'django-rest-swagger',
                      'djangorestframework_simplejwt', 'Pillow', 'sorl-thumbnail', 'sorl-thumbnail-serializer-field'],
    license="MiT",
    keywords="www website etc",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MiT",
    ]
)

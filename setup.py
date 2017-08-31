#!/usr/bin/env python
try:
    from setuptools import setup, find_packages
    packages = find_packages(exclude=['tests'])
except ImportError:
    from distutils.core import setup
    packages = ["pyLinguist"]

setup(
    name="pyLinguist",
    packages=packages,
    version="0.1.2",
    description="Yandex Linguistics APIs for Python 3.3+",
    long_description="Yandex Linguistics APIs for Python 3.3+",
    author="hell03end",
    author_email="hell03end@outlook.com",
    url="https://github.com/hell03end/pyYandexLinguistics",
    keywords="translate dictionary predict predictor yandex linguistics "
             "yandex-translate yandex-dictionary yandex-predictor speller"
             "spelling grammar yandex-speller",
    classifiers=[
        "Intended Audience :: Developers",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.3",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    license="MIT License",
    platforms=["All"],
    install_requires="requests>=2.2",
    python_requires=">=3.3"
)

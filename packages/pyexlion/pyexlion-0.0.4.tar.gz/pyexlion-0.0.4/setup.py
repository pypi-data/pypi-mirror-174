#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyexlion",
    version="0.0.4",
    author="patrickxu",
    author_email="xcpxcp198608@163.com",
    description="lion package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/patrickxu1986/pylion",
    project_urls={
        "Bug Tracker": "https://github.com/patrickxu1986/pylion/issues",
    },
    install_requires=[
        'pygalaxy>=0.3.6',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",

)

# deploy project to pypi
# pip3 install --upgrade build
# python3 -m build
# pip3 install --upgrade twine
# python3 -m twine upload --repository pypi dist/*

# -*- coding: utf-8 -*-

"""
Package setup.

Set me up with `python setup.py bdist_wheel --universal`
"""
import io

from setuptools import setup

# Get long description from readme
with io.open("README.md", "rt", encoding="utf8") as readmefile:
    README = readmefile.read()

setup(
    name="gh-pr-update-description",
    version="0.1.4",
    description="Update Github PR description with top commit title + body",
    author="Noah Pendleton",
    author_email="2538614+noahp@users.noreply.github.com",
    url="https://github.com/noahp/gh-pr-update-description",
    project_urls={
        "Code": "https://github.com/noahp/gh-pr-update-description",
        "Issue tracker": "https://github.com/noahp/gh-pr-update-description/issues",
    },
    long_description=README,
    long_description_content_type="text/markdown",
    install_requires=["click", "gitpython", "pygithub"],
    # using markdown as pypi description:
    # https://dustingram.com/articles/2018/03/16/markdown-descriptions-on-pypi
    setup_requires=["setuptools>=38.6.0", "wheel>=0.31.0", "twine>=1.11.0"],
    py_modules=["gh_pr_update_description"],
    entry_points={
        "console_scripts": ["gh-pr-update-description = gh_pr_update_description:main"]
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
)
#!/usr/bin/env python3
"""
Setup script for Enterprise AppData Deep Clean Suite
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="enterprise-appdata-cleaner",
    version="1.2.0",
    author="Enterprise AppData Cleaner Team",
    author_email="touyboateng339@gmail.com",
    description="Enterprise-grade AppData cleanup tool with security and compliance features",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/tonycondone/enterprise-appdata-cleaner",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
        "Topic :: Security",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "appdata-cleaner=cleaner:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="appdata cleanup enterprise security compliance windows",
    project_urls={
        "Bug Reports": "https://github.com/tonycondone/enterprise-appdata-cleaner/issues",
        "Source": "https://github.com/tonycondone/enterprise-appdata-cleaner",
        "Documentation": "https://github.com/tonycondone/enterprise-appdata-cleaner/wiki",
    },
) 
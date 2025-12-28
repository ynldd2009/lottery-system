#!/usr/bin/env python3
"""
Setup script for Lottery Analysis and Prediction System.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_path = Path(__file__).parent / "README.md"
if readme_path.exists():
    with open(readme_path, 'r', encoding='utf-8') as f:
        long_description = f.read()
else:
    long_description = "Lottery Analysis and Prediction System"

# Read requirements
requirements_path = Path(__file__).parent / "requirements.txt"
if requirements_path.exists():
    with open(requirements_path, 'r', encoding='utf-8') as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
else:
    requirements = []

setup(
    name="lottery-analysis-system",
    version="1.0.0",
    author="Lottery System Team",
    author_email="contact@lotteryanalysis.org",
    description="A cross-platform lottery analysis and prediction system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ynldd2009/lottery-system",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Games/Entertainment",
        "Topic :: Scientific/Engineering :: Mathematics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Environment :: X11 Applications :: Qt",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'lottery-analysis=main:main',
            'lottery-demo=demo_cli:main',
        ],
    },
    include_package_data=True,
    package_data={
        '': ['*.json', '*.md'],
    },
    keywords="lottery analysis prediction statistics data-science",
    project_urls={
        "Bug Reports": "https://github.com/ynldd2009/lottery-system/issues",
        "Source": "https://github.com/ynldd2009/lottery-system",
    },
)

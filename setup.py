"""
Setup script for GitBrowse.
"""

import os
from setuptools import setup, find_packages

# Get the long description from the README file
with open(os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# Get the version from the package
version = "4.0.0"  # Default version if not found
try:
    with open(os.path.join("gitbrowse", "__init__.py"), encoding="utf-8") as f:
        for line in f:
            if line.startswith("__version__"):
                version = line.split("=")[1].strip().strip('"\'')
                break
except (FileNotFoundError, IOError):
    pass

setup(
    name="gitbrowse",
    version=version,
    description="A powerful command-line tool for browsing GitHub repositories",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="SimpleDioney",
    author_email="contato@dioneygabriel.com.br",
    url="https://github.com/SimpleDioney/gitbrowse",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests>=2.25.0",
        "beautifulsoup4>=4.9.3",
        "colorama>=0.4.4",
        "pygments>=2.7.3",
        "rich>=10.0.0",
        "tqdm>=4.56.0",
        "click>=8.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.2.2",
            "black>=21.5b2",
            "isort>=5.8.0",
            "flake8>=3.9.1",
            "mypy>=0.812",
            "pytest-cov>=2.12.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "gitbrowse=gitbrowse.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    keywords="github, git, cli, browse, terminal",
)
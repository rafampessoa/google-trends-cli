import os
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

def read_requirements(filename):
    """Read requirements from a file."""
    with open(os.path.join("requirements", filename), "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("-r") and not line.startswith("#")]

# Get requirements from files
install_requires = read_requirements("base.txt")
api_requires = read_requirements("api.txt") 
dev_requires = read_requirements("development.txt")

# Remove base requirements from api_requires to avoid duplication
api_requires = [req for req in api_requires if req not in install_requires]

# Remove base and api requirements from dev_requires to avoid duplication
dev_requires = [req for req in dev_requires if req not in install_requires and req not in api_requires]

extras_require = {
    'dev': dev_requires,
    'api': api_requires,
    'all': api_requires + dev_requires,
}

setup(
    name="gtrends-cli",
    version="0.2.0",
    author="Mohammed A. Al-Kebsi",
    author_email="mohammed.k@mohammed-al-kebsi.space",
    description="CLI and API tools for Google Trends data analysis and content suggestions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Nao-30/google-trends-cli",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            "gtrends=gtrends_cli.main:main",
            "gtrends-api=gtrends_api.main:start_api",
        ],
    },
    extras_require=extras_require,
)

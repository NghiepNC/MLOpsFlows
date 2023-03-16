"""The setup module"""
from pathlib import Path

from setuptools import find_namespace_packages, setup

# Load packages from requirements.txt
BASE_DIR = Path(__file__).parent
with open(Path(BASE_DIR, "requirements.txt"), encoding="UTF-8") as file:
    required_packages = [ln.strip() for ln in file.readlines()]

test_packages = [
    "pytest==7.1.2",
    "pytest-cov==4.0.0",
    "pytest-html-reporter==0.2.9",
]

style_packages = [
    "black==22.6.0",
    "flake8==4.0.1",
    "isort==5.9.3",
    "pre-commit==2.19.0",
]

docs_packages = [
    "mkdocs==1.4.2",
    "mkdocs-material==8.2.15",
    "mkdocstrings==0.20.0",
    "mkdocstrings-python==0.8.3",
]
# Define our package
setup(
    name="mlopsflows",
    version=0.1,
    description="MLOpsFlows projects.",
    author="nam.nd.00",
    author_email="nam.nd.00@gmail.com",
    url="https://namnd00.github.io/MLOpsFlows/",
    python_requires=">=3.8",
    packages=find_namespace_packages(),
    install_requires=[required_packages],
    extras_require={
        "dev": docs_packages + style_packages + test_packages,
        "docs": docs_packages,
        "test": test_packages,
    },
)

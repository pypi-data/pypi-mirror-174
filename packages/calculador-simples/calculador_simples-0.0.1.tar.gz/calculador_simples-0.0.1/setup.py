from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="calculador_simples",
    version="0.0.1",
    author="gabriel_rodrigues_ferraz_da_silva",
    author_email="gabrielcma_@hotmail.com",
    description="Calculadora simples feita em Python",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gabrielferrazs/calculadora_simples",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.6',
)
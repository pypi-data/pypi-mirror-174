from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="basic_ops_calculator",
    version="0.0.1",
    author="Marcelo L Valerio",
    author_email="mar.valerio@hotmail.com.br",
    description="A basic calculator, to test the package creation",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Marcelo-L-Valerio/DIO-DataScience-Bootcamp/tree/main/02-Criacao-de-pacotes",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)
from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="operacoes_matematicas_teste",
    version="0.0.3",
    author="Ricardo Duarte",
    author_email="rykardo.contato@gmail.com",
    description="Pacote python que faz operações matemáticas simples",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rykardoassets/operacoes_matematicas",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)
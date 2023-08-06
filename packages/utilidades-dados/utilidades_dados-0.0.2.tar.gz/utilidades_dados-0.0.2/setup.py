from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="utilidades_dados",
    version="0.0.2",
    author="my_name",
    author_email="caiena.danilo@gmail.com",
    description="Pacote de cálculos simples e para tratamento de dados.",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rdaniloc/utilidade-dados-package.git",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)

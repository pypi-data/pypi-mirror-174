# verifica a instalação da biblioteca setuptools

from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="contatos",
    version="0.0.1",
    author="Ubiratan Tavares",
    author_email="ust1973@gmail.com",
    description="sistema de contato",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ubiratantavares/projeto_sistema_contato",  # inserir a url do projeto no github
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.9',
)

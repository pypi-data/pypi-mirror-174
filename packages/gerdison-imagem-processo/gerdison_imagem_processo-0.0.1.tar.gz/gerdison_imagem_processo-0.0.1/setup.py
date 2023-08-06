from setuptools import setup, find_packages

with open("README.md", "r") as f:           # Aponta para página com a descrição longa da descrição do pacote
    page_description = f.read()

with open("requirements.txt") as f:         # Aponta para o carregamento automático dos requerimentos para uso do pacote
    requirements = f.read().splitlines()

setup(
    name = "gerdison_imagem_processo",
    version = "0.0.1",
    author = "Gerdison",
    author_email = "gerdison.dona@gmail.com",
    description = "Pacote de Processamento de imagens",
    long_description = page_description,
    long_description_content_type = "text/markdown",
    packages = find_packages(),
    install_requires = requirements,
    python_requires = '>=3.8',
)

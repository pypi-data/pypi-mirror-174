from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="estrutura_de_dados",
    version="0.0.1",
    author="dev-rafa1707",
    author_email="rafa1707@gmail.com",
    description="Estrutura de Dados",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dev-rafa1707/estrutura_de_dados",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)

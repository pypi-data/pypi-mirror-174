from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="DescomplicandoACriacaoDePacotes",
    version="0.0.1",
    author="Carlos Valenca",
    author_email="cavac10@yahoo.com.br",
    description="DIO Project",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CarlVAC1980/DescomplicandoACriacaoDePacotesEmPython",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)
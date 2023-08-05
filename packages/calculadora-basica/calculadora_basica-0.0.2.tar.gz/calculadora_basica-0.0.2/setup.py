from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="calculadora_basica",
    version="0.0.2",
    author="FawkesC05",
    author_email="fawkesc05@gmail.com",
    description="Uma simples calculadora GUI",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FawkesC05/DIO-repo/tree/main/Geracao-Tech_Unimed-BH_DS/calculadora_basica",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)

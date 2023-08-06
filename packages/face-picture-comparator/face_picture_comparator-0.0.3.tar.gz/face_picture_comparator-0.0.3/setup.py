from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="face_picture_comparator",
    version="0.0.3",
    author="Ronaldo Nunes",
    author_email="projetoftnunes@gmail.com",
    description="Two face comparison pack",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ronaldo-Nunes/Cursos/tree/main/Geracao-Tech-Unimed-BH-Ciencia-Dados/compare-faces-package",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8'
)
    
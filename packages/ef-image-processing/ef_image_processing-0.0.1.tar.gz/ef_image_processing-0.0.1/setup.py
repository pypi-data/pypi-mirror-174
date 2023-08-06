from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

#with open("requirements.txt") as f:
#    requirements = f.read().splitlines()

setup(
    name="ef_image_processing",
    version="0.0.1",
    author="Elpidio",
    author_email="eferreira1@gmail.com",
    description="Color change from original project image to reference image color",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eferreira50/dio-desafio-github-primeiro-repositorio/Desafio-de-Projeto/image-processing-package", 
    packages=find_packages(),
    #install_requires=requirements,
    install_requires=['matplotlib', 'numpy', 'scikit-image>=0.16.1'],
    python_requires='>=3.9',
)
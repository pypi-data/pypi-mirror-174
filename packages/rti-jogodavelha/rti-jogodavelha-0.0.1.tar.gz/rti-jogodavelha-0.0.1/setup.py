from setuptools import find_packages, setup

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name='rti-jogodavelha',
    version='0.0.1',
    author='Mauro Robson Tazinaffo',
    author_email='robsontazinaffo@hotmail.com',
    description=u'Exemplo de jogo da velha em python',
    long_description=page_description,
    long_description_content_type="text/markdown",
    url='https://github.com/robson-tazinaffo/ciencia-dados-python/'
        'tree/main/modulo2/Desafio2',
    license='MIT License',
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)

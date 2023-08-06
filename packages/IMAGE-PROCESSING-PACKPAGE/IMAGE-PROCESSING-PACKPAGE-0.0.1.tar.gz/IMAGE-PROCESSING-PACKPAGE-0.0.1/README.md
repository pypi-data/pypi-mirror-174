# image_processing

Description.
The package image_processing is used to:
    Processing:
        - Histogram matching
        - Structural similarity
        - Resize image
    Utils:
        - Read image
        - Save image
        - Plot image
        - Plot result
        - plot histogram


## Installation

Use the package manager [pip](http://pip.pypa.io/en/stable/) to install package_name


***bash
pip install package_name
***

## Usage

***python
from package_name.modulo1_name import file1_name
file1_name.my_function()

## Author
Matheus














Desafio-002 : Pacote de Processamento de Imagens
Descrição
Esse projeto consiste na criação de um pacote para python, com base no curso ministrado por Karina Kato.
É apenas um pacote de exemplo, baseado no scikit-image
Anotações das aulas podem ser vistas aqui.
Passos para a hospedagem no Pypi
Primeiro se realiza uma instalação ou upgrade do pip, twine, setuptools e wheel
remova a opção --user se não deseja instalar no user.home ou esteja usando um venv.
python -m pip install --upgrade pip
python -m pip install --user twine
python -m pip install --user setuptools
python -m pip install --user wheel
Cria-se as distribuições
python setup.py sdist bdist_wheel
Serão criadas 3 pastas no projeto:
build
dist
image_processing_package.egg-info
O próximo passo é o upload no Test Pypi.
python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
O comando para upload no Pypi é:
python -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
Instalação
Para a instalação local, é necessário instalar os requerimentos primeiro.
pip install -r requirements.txt
Para a instalação do pacote, basta usar o pip direcionando para o image-processing-test-package

pip install image-processing-test-package==0.0.2
Uso
Basta importar os módulos de acordo com o que deseja
from image-processing-test-package.processing import transformation
transformation.resize_image(image1, 0.5)
Autor
Matheus Lacerda

Licença
MIT
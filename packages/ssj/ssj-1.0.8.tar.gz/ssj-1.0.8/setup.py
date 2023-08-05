from setuptools import setup
setup(name = 'ssj',
version = '1.0.8',
author = 'Jonathan N. Nagel',
author_email = 'jinnascimento81@gmail.com',
install_requires = ['dropbox', 'tinydb', 'nested_dict', 'cryptography'],
packages = ['ssj'],
long_description='Um servidor de NoSQL baseado em JSON e dicionarios Python que facilita o uso em rede local ou em maquina local.',
description = 'Servidor ou gestor de dados em JSON.',
license = 'MIT',
keywords = 'ssj')

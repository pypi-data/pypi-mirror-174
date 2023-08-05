from setuptools import setup
setup(name = 'ssj',
version = '1.0.6',
author = 'Jonathan N. Nagel',
author_email = 'jinnascimento81@gmail.com',
install_requires = ['dropbox', 'tinydb', 'nested_dict', 'cryptography'],
packages = ['ssj'],
description = 'Servidor ou gestor de dados em JSON.',
license = 'MIT',
keywords = 'ssj')

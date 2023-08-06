# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_bdd_context']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'py-bdd-context',
    'version': '0.0.1',
    'description': 'Biblioteca com Context Manager para facilitar os testes de Behavior Driven Development (BDD)',
    'long_description': '# py-bdd-context\n\nBiblioteca com Context Manager para facilitar os testes de Behavior Driven Development (BDD).\n\nEssa biblioteca irá te ajudar a organizar os seus testes!\n\n## Utilizando\nExistem exemplos de como utilizar a lib na pasta `examples`.\n\n',
    'author': 'Imobanco',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/imobanco/py-bdd-context',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

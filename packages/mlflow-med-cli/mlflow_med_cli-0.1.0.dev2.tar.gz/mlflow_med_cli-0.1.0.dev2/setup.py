# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mlflow_med_cli', 'mlflow_med_cli.examples.sklearn']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.6.1,<4.0.0',
 'mlflow>=1.29.0,<2.0.0',
 'rich>=12.6.0,<13.0.0',
 'ruamel-yaml>=0.17.21,<0.18.0',
 'scikit-learn>=1.1.2,<2.0.0',
 'typer>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['mlflow-med-cli = mlflow_med_cli.main:app']}

setup_kwargs = {
    'name': 'mlflow-med-cli',
    'version': '0.1.0.dev2',
    'description': '',
    'long_description': '# MLFlow-med-cli\n\nCLI tool for MLFlow-med experiment management.\n',
    'author': 'hossay',
    'author_email': 'youhs4554@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

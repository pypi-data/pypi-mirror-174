# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mylearn']

package_data = \
{'': ['*']}

install_requires = \
['apache-airflow[postgres]>=2.4.2,<3.0.0',
 'pandas>=1.5.1,<2.0.0',
 'psycopg2>=2.9.5,<3.0.0']

setup_kwargs = {
    'name': 'mylearn',
    'version': '0.0.2',
    'description': 'mylearn: my Machine Learning framework',
    'long_description': '<h2 align="center">mylearn: my Machine Learning framework</h2>\n\n<p align="center">\n<a href="https://pypi.org/project/mylearn"><img src="https://img.shields.io/pypi/v/mylearn.svg"></a>\n<a href="https://pypi.org/project/mylearn"><img src="https://img.shields.io/pypi/pyversions/mylearn.svg"></a>\n<a href="https://github.com/MichaelKarpe/mylearn/blob/main/LICENSE"><img src="https://img.shields.io/pypi/l/mylearn.svg"></a>\n<a href="https://github.com/MichaelKarpe/mylearn/actions"><img src="https://github.com/MichaelKarpe/mylearn/workflows/ci/badge.svg"></a>\n<a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n</p>\n\n___\n\n[mylearn](https://github.com/MichaelKarpe/mylearn) is a Machine Learning framework based on\n[Airflow](https://github.com/apache/airflow) and [MLflow](https://github.com/mlflow/mlflow) for designing machine\nlearning systems in a production perspective.\n\n**Work in progress... Stay tuned!**\n\n# Index\n\n1. [Prerequisites](#prerequisites)\n2. [Installation & Setup](#installation-setup)\n3. [Usage](#usage)\n\n# Prerequisites\n\n## pyenv\n\nTo be completed with how to install and setup pyenv\n\n## poetry\n\nTo be completed with how to install and setup poetry\n\n# Installation & Setup\n\nmylearn leverages [poetry](https://github.com/python-poetry/poetry) and [poethepoet](https://github.com/nat-n/poethepoet)\nto make its installation and setup surprisingly simple.\n\n## Installation\n\nIt is recommended to install requirements within a virtualenv located at the project root level, although not required.\n```commandline\npoetry config virtualenvs.in-project true\n```\n\nInstallation is run with\n```commandline\npoetry install\n```\n\n## Airflow Setup\n\nAirflow setup is initialized via a `poe` command\n```commandline\npoe airflow-init\n```\n\nAirflow Scheduler & Webserver can be run with\n```commandline\npoe airflow-scheduler\npoe airflow-webserver\n```\n\nAirflow UI can be opened at [localhost](0.0.0.0:8080) (port 8080), and you can login with username and password `admin`.\n\nIf you want to clean your Airflow setup before rerunning `poe airflow-init`, you need to kill Airflow Scheduler &\nWebserver and run\n```commandline\npoe airflow-clean\n```\n\n## MLflow Setup\n\nMLflow UI can be opened at [localhost](0.0.0.0:5000) (port 5000) after execution of the following command:\n```commandline\npoe mlflow-ui\n```\n\n# Usage\n\n## MLflow Pipelines Regression Template\n\nThe *mlflow-template* pipeline, based on the\n[MLflow Pipelines Regression Template](https://github.com/mlflow/mlp-regression-template), can be run independently with\n```commandline\npoe mlflow-run\n```\n\nor via an Airflow Directed Acyclic Graph (DAG) by triggering the *mlflow-template* DAG via Airflow UI or with\n```commandline\nTO BE COMPLETED\n```\n\n## Other examples\n\n**Work in progress... Stay tuned!**\n',
    'author': 'Michael Karpe',
    'author_email': 'michael.karpe@berkeley.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/MichaelKarpe/mylearn',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<3.12',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['secrets_env', 'secrets_env.auth', 'secrets_env.cli', 'secrets_env.config']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'hvac>=0.11.2,<0.12.0',
 'keyring>=23.3.0,<24.0.0',
 'requests>=2.21.0,<3.0.0']

extras_require = \
{'all': ['PyYAML>=5.1.2,<7'],
 'all:python_version < "3.11"': ['tomli>=1.1.0,<3'],
 'toml:python_version < "3.11"': ['tomli>=1.1.0,<3'],
 'yaml': ['PyYAML>=5.1.2,<7']}

entry_points = \
{'console_scripts': ['secrets.env = secrets_env.cli:main'],
 'poetry.application.plugin': ['poetry-secrets-env-plugin = '
                               'secrets_env.poetry:SecretsEnvPlugin']}

setup_kwargs = {
    'name': 'secrets-env',
    'version': '0.12.0',
    'description': 'Put secrets from Vault to environment variables',
    'long_description': "# Secrets.env 🔓\n\n[![PyPI version](https://img.shields.io/pypi/v/secrets.env)](https://pypi.org/project/secrets-env/)\n![Python version](https://img.shields.io/pypi/pyversions/secrets.env)\n[![test result](https://img.shields.io/github/workflow/status/tzing/secrets.env/Tests)](https://github.com/tzing/secrets.env/actions/workflows/test.yml)\n\nPut secrets from [Vault](https://www.vaultproject.io/) KV engine to environment variables like a `.env` loader, without not landing data on disk.\n\n![screenshot](./docs/imgs/screenshot.png)\n\nSecurity is important, but don't want it to be a stumbling block. We love secret manager, but the practice of getting secrets for local development could be a trouble.\n\nThis app is built to *plug in* secrets into development without landing data on disk, easily reproduce the environment, and reduce the risk of uploading the secrets to the server.\n\n\n* 📦 [PyPI](https://pypi.org/project/secrets-env/)\n* 📐 [Source code](https://github.com/tzing/secrets.env)\n* 📗 [Documentation](https://tzing.github.io/secrets.env/)\n",
    'author': 'tzing',
    'author_email': 'tzingshih@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tzing/secrets.env',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

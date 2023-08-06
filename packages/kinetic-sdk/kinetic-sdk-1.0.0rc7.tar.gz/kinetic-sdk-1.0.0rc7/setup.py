# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['kinetic_sdk',
 'kinetic_sdk.generated',
 'kinetic_sdk.generated.kinetic-sdk-generated.kinetic_sdk_generated',
 'kinetic_sdk.generated.kinetic-sdk-generated.kinetic_sdk_generated.api',
 'kinetic_sdk.generated.kinetic-sdk-generated.kinetic_sdk_generated.apis',
 'kinetic_sdk.generated.kinetic-sdk-generated.kinetic_sdk_generated.model',
 'kinetic_sdk.generated.kinetic-sdk-generated.kinetic_sdk_generated.models',
 'kinetic_sdk.generated.test',
 'kinetic_sdk.helpers',
 'kinetic_sdk.models']

package_data = \
{'': ['*'],
 'kinetic_sdk.generated': ['.openapi-generator/*',
                           'docs/*',
                           'kinetic-sdk-generated/*']}

install_requires = \
['kinetic-sdk-generated>=1.0.0-rc.1,<2.0.0',
 'pybase64>=1.2.2,<2.0.0',
 'pybip39>=0.1.0,<0.2.0',
 'solana>=0.27.2,<0.28.0',
 'solders==0.9.3']

setup_kwargs = {
    'name': 'kinetic-sdk',
    'version': '1.0.0rc7',
    'description': '',
    'long_description': "# kinetic-python\n\nPython SDK implementation to use [Kinetic](https://kinetic.kin.org/) by [Kin Foundation](https://kin.org/)\n\n## Installation\n\n```\npip install kinetic-sdk\n```\n\n## Usage\n\n### Initialization\n\n```py\nimport kinetic_sdk\n\nenvironment = 'devnet'\napp_index = 1\nsdk = kinetic_sdk.KineticSdk.setup(environment, app_index)\n```\n\n### Get Account History\n\n```py\nhistory = sdk.get_history(account_public_key, mint_public_key)\n```\n\n### Get Token Accounts\n\n```py\ntoken_accounts = sdk.get_token_accounts(account_public_key, mint_public_key)\n```\n\n### Request Airdrop\n\n```py\nairdrop = sdk.request_airdrop(account_public_key, amount_str, mint_public_key)\n```\n\n### Create Account\n\n```py\nowner = Keypair.generate()\naccount = sdk.create_account(owner, mint_public_key)\n```\n\n### Make Transfer\n\n```py\ntx = sdk.make_transfer(\n    owner=alice_keypair,\n    destination=bob_public_key, \n    amount=1, \n    mint=mint_public_key, \n    tx_type=TransactionType.NONE\n)\n```\n\n# Documentation\n\nThis [file](https://github.com/kin-labs/kinetic-python/blob/main/src/__main__.py) can be followed for sample code, but more documentation and samples be [here](https://314-refactor-for-kinetic.kin-developer-docs.pages.dev/developers/python/).\n\n# Development\n\nClone this request\n\n```\ngit clone git@github.com:kin-labs/kinetic-python.git\n```\n\nInstall the dependencies, the project uses [Poetry](https://python-poetry.org/), so you don't need to worry about creating virtual environments because it will create it for you.\n```\nmake install\n```\n\nRun test\n\n```\nmake test\n```\n\n",
    'author': 'Kin Foundation',
    'author_email': 'dev@kin.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kin-labs/kinetic-python-sdk',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

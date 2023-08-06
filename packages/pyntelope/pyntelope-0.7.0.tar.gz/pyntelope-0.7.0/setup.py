# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyntelope', 'pyntelope.types']

package_data = \
{'': ['*']}

install_requires = \
['base58>=2.1.1,<3.0.0',
 'httpx>=0.22',
 'pycryptodome>=3.15.0,<4.0.0',
 'pydantic>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'pyntelope',
    'version': '0.7.0',
    'description': 'Interact with Antelope blockchains',
    'long_description': '<div align="center">\n    \n<p align="center">\n  <img width="600" src="https://miro.medium.com/max/1400/1*5KEvJB1UBBsk_1ZTBtJfJA.png">\n</p>\n    \n*Minimalist python library to interact with antelope blockchain networks*\n \n![Test](https://github.com/FACINGS/pyntelope/actions/workflows/main_workflow.yml/badge.svg)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyntelope)\n![version](https://img.shields.io/pypi/v/pyntelope)\n![GitHub repo size](https://img.shields.io/github/repo-size/facings/pyntelope)\n![GitHub last commit](https://img.shields.io/github/last-commit/facings/pyntelope)\n\n</div>\n\n# What is it?\n**pyntelope** is a python library to interact with Antelope blockchains.  \nIts main focus are server side applications.  \nThis library is heavily influenced by [µEOSIO](https://github.com/EOSArgentina/ueosio). Many thanks to them for the astonishing job!  \n\n\n# Main features\n- Send transactions\nIts main usage today is to send transactions to the blockchain\n- Statically typed\nThis library enforces and verifies types and values.\n- Serialization\n**pyntelope** serializes the transaction before sending to the blockchain. \n- Paralellization\nAlthough python has the [GIL](https://realpython.com/python-gil/) we try to make as easier as possible to paralellize the jobs.  \nAll data is as immutable and all functions are as pure as we can make them.  \n\n\n# Stability\nThis work is in alpha version. That means that we make constant breaking changes to its api.  \nAlso there are known (and, of course unknown) bugs and various limitations.  \nGiven that, we at [FACINGS](https://facings.io/) have been using this library in production for over an year now.  \nHowever we\'d advise for you to fix its version when deploying to prod.  \n\n\n# Using\nJust `pip install pyntelope` and play around.  \n(we don\'t support, and have no plans to support [conda](https://docs.conda.io/en/latest/))  \nRather then starting with long docs, just a simple example:  \n\n\n## Use Send Message action\n```python\nimport pyntelope\n\n\nprint("Create Transaction")\ndata=[\n    pyntelope.Data(\n        name="from",\n        value=pyntelope.types.Name("me.wam"), \n    ),\n    pyntelope.Data(\n        name="message",\n         value=pyntelope.types.String("hello from pyntelope"),\n    ),\n]\n\nauth = pyntelope.Authorization(actor="me.wam", permission="active")\n\naction = pyntelope.Action(\n    account="me.wam", # this is the contract account\n    name="sendmsg", # this is the action name\n    data=data,\n    authorization=[auth],\n)\n\nraw_transaction = pyntelope.Transaction(actions=[action])\n\nprint("Link transaction to the network")\nnet = pyntelope.WaxTestnet()  # this is an alias for a testnet node\n# notice that pyntelope returns a new object instead of change in place\nlinked_transaction = raw_transaction.link(net=net)\n\n\nprint("Sign transaction")\nkey = "a_very_secret_key"\nsigned_transaction = linked_transaction.sign(key=key)\n\n\nprint("Send")\nresp = signed_transaction.send()\n\nprint("Printing the response")\nresp_fmt = json.dumps(resp, indent=4)\nprint(f"Response:\\n{resp_fmt}")\n```\n\nThere are some other examples [here](./examples)\n\n\n# Known bugs\n### multi-byte utf-8 characters can not be serialized\n- Serialization of multi-byte utf-8 characters is somewhat unpredictable in the current implementation, therfore any String input containing multi-utf8 byte characters will be blocked for the time being.\n\n\n# Contributing\nAll contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome.  \nIf you find a bug, just open a issue with a tag "BUG".  \nIf you want to request a new feature, open an issue with a tag "ENH" (for enhancement).  \nIf you feel like that our docs could be better, please open one with a tag "DOC".  \nAlthough we have the next few steps already planned, we are happy to receive the community feedback to see where to go from there.  \n\n\n### Development\nIf you want to develop for **pyntelope**, here are some tips for a local development environment.\nWe\'ll be more then happy to receive PRs from the community.\nAlso we\'re going full [Black](https://black.readthedocs.io/en/stable/) and enforcing [pydocstyle](http://www.pydocstyle.org/en/stable/) and [isort](https://pypi.org/project/isort/) (with the limitations described in the .flake8 file)\n\n#### Setup\nCreate a virtual env\nEnsure the dependencies are met:\n```\npip install poetry\npoetry install\n```\n\n#### Run tests\nThe tests are run against a local network.  \nBefore running the tests you\'ll need to `docker-compose up` to create the local network, users and contracts used in the tests.  \nWhen ready, just:\n```\npytest\n```\n\n\n\n',
    'author': 'Team',
    'author_email': 'pyntelope@facings.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/FACINGS/pyntelope',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

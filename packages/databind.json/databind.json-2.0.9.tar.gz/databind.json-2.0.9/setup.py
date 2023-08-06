# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['json']

package_data = \
{'': ['*']}

install_requires = \
['databind.core>=2.0.9,<3.0.0',
 'nr.util>=0.8.6,<1.0.0',
 'typing-extensions>=3.10.0']

setup_kwargs = {
    'name': 'databind.json',
    'version': '2.0.9',
    'description': 'De-/serialize Python dataclasses to or from JSON payloads. Compatible with Python 3.7 and newer.',
    'long_description': '# databind.json\n\nThe `databind.json` package implements the de-/serialization to or from JSON payloads using\nthe `databind.core` framework.\n\n## Quickstart\n\n```py\nimport databind.json\nimport dataclasses\n\n@dataclasses.dataclass\nclass ServerConfig:\n  host: str\n  port: int = 8080\n\n@dataclasses.dataclass\nclass MainConfig:\n  server: ServerConfig\n\npayload = { \'server\': { \'host\': \'127.0.0.1\' } }\nconfig = databind.json.load(payload, MainConfig)\nassert config == MainConfig(ServerConfig(\'127.0.0.1\'))\n```\n\n## Examples for common use cases\n\n### Unions with literal matches\n\n```py\nimport dataclasses\nimport databind.json\nfrom typing import Literal\n\n@dataclasses.dataclass\nclass AwsMachine:\n  region: str\n  name: str\n  instance_id: str\n  provider: Literal["aws"] = "aws"\n\n@dataclasses.dataclass\nclass AzureMachine:\n  resource_group: str\n  name: str\n  provider: Literal["azure"] = "azure"\n\nMachine = AwsMachine | AzureMachine\n\npayload = {"provider": "azure", "resource_group": "foo", "name": "bar"}\nassert databind.json.load(payload) == AzureMachine("foo", "bar")\n```\n\n---\n\n<p align="center">Copyright &copy; 2020 &ndash; Niklas Rosenstein</p>\n',
    'author': 'Niklas Rosenstein',
    'author_email': 'rosensteinniklas@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

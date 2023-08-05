# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['named']

package_data = \
{'': ['*']}

install_requires = \
['typing-extensions>=4.3.0']

setup_kwargs = {
    'name': 'named',
    'version': '1.0.1',
    'description': 'Named types.',
    'long_description': '# `named`\n\n[![License][License Badge]][License]\n[![Version][Version Badge]][Package]\n[![Downloads][Downloads Badge]][Package]\n[![Discord][Discord Badge]][Discord]\n\n[![Documentation][Documentation Badge]][Documentation]\n[![Check][Check Badge]][Actions]\n[![Test][Test Badge]][Actions]\n[![Coverage][Coverage Badge]][Coverage]\n\n> *Named types.*\n\n## Installing\n\n**Python 3.7 or above is required.**\n\n### pip\n\nInstalling the library with `pip` is quite simple:\n\n```console\n$ pip install named\n```\n\nAlternatively, the library can be installed from source:\n\n```console\n$ git clone https://github.com/nekitdev/named.git\n$ cd named\n$ python -m pip install .\n```\n\n### poetry\n\nYou can add `named` as a dependency with the following command:\n\n```console\n$ poetry add named\n```\n\nOr by directly specifying it in the configuration like so:\n\n```toml\n[tool.poetry.dependencies]\nnamed = "^1.0.1"\n```\n\nAlternatively, you can add it directly from the source:\n\n```toml\n[tool.poetry.dependencies.named]\ngit = "https://github.com/nekitdev/named.git"\n```\n\n## Example\n\n```python\nfrom named import get_name, get_type_name, is_named\n\nprint(is_named(int))      # True\nprint(get_name(int))      # int\n\nprint(is_named(42))       # False\nprint(get_type_name(42))  # int\n```\n\n## Documentation\n\nYou can find the documentation [here][Documentation].\n\n## Support\n\nIf you need support with the library, you can send an [email][Email]\nor refer to the official [Discord server][Discord].\n\n## Changelog\n\nYou can find the changelog [here][Changelog].\n\n## Security Policy\n\nYou can find the Security Policy of `named` [here][Security].\n\n## Contributing\n\nIf you are interested in contributing to `named`, make sure to take a look at the\n[Contributing Guide][Contributing Guide], as well as the [Code of Conduct][Code of Conduct].\n\n## License\n\n`named` is licensed under the MIT License terms. See [License][License] for details.\n\n[Email]: mailto:support@nekit.dev\n\n[Discord]: https://nekit.dev/discord\n\n[Actions]: https://github.com/nekitdev/named/actions\n\n[Changelog]: https://github.com/nekitdev/named/blob/main/CHANGELOG.md\n[Code of Conduct]: https://github.com/nekitdev/named/blob/main/CODE_OF_CONDUCT.md\n[Contributing Guide]: https://github.com/nekitdev/named/blob/main/CONTRIBUTING.md\n[Security]: https://github.com/nekitdev/named/blob/main/SECURITY.md\n\n[License]: https://github.com/nekitdev/named/blob/main/LICENSE\n\n[Package]: https://pypi.org/project/named\n[Coverage]: https://codecov.io/gh/nekitdev/named\n[Documentation]: https://nekitdev.github.io/named\n\n[Discord Badge]: https://img.shields.io/badge/chat-discord-5865f2\n[License Badge]: https://img.shields.io/pypi/l/named\n[Version Badge]: https://img.shields.io/pypi/v/named\n[Downloads Badge]: https://img.shields.io/pypi/dm/named\n\n[Documentation Badge]: https://github.com/nekitdev/named/workflows/docs/badge.svg\n[Check Badge]: https://github.com/nekitdev/named/workflows/check/badge.svg\n[Test Badge]: https://github.com/nekitdev/named/workflows/test/badge.svg\n[Coverage Badge]: https://codecov.io/gh/nekitdev/named/branch/main/graph/badge.svg\n',
    'author': 'nekitdev',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/nekitdev/named',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)

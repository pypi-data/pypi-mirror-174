# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['driftpy', 'driftpy.constants', 'driftpy.idl', 'driftpy.math', 'driftpy.setup']

package_data = \
{'': ['*']}

install_requires = \
['anchorpy==0.10.0',
 'requests>=2.28.1,<3.0.0',
 'solana>=0.25.0,<0.26.0',
 'types-requests>=2.28.9,<3.0.0']

setup_kwargs = {
    'name': 'driftpy',
    'version': '0.6.5',
    'description': 'A Python client for the Drift DEX',
    'long_description': '# DriftPy\n\n<div align="center">\n    <img src="https://camo.githubusercontent.com/d41b63c668d34e0ac5baba28a6fcff818da7b168752e511a605096dd9ba94039/68747470733a2f2f75706c6f6164732d73736c2e776562666c6f772e636f6d2f3631313538303033356164353962323034333765623032342f3631366639376134326635363337633435313764303139335f4c6f676f2532302831292532302831292e706e67" width="30%" height="30%">\n</div>\n\nDriftPy is the Python client for the [Drift](https://www.drift.trade/) protocol. It allows you to trade and fetch data from Drift using Python.\n\n[Read The Documentation](https://drift-labs.github.io/driftpy/)\n\n## Installation\n\n```\npip install driftpy\n```\n\nNote: requires Python >= 3.9.\n\n## Examples\n\n[Arbitrage Trading](https://github.com/0xbigz/driftpy-arb)\n\n[Querying and Visualization](https://gist.github.com/mcclurejt/b244d4ca8b0000ce5078ef8f60e937d9)\n\n## Development\n\n- `git submodule update --init --recursive`\n- cd protocol-v2 && yarn \n- cd sdk && yarn && yarn build && cd .. \n- anchor build \n- in deps/serum/dex run `cargo build-bpf`\n- update anchor IDL for v2 protocol on new re-builds (copy new idls to src/driftpy/idl/...json)\n- run python tests: `bash test.sh v2tests/test.py`\n\n### Development Setup\n\nIf you want to contribute to DriftPy, follow these steps to get set up:\n\n1. Install [poetry](https://python-poetry.org/docs/#installation)\n2. Install dev dependencies (in local env):\n```sh\npoetry install\n```\n\n### Testing\n\n1. `bash test.sh`\n\n### Building the docs\n\nRun `mkdocs serve` to build the docs and serve them locally.\n\n### Releasing a new version of the package\n\n1. Make sure CHANGELOG.md is updated.\n2. Run `bumpversion major|minor|patch` to update the version number locally and create a tagged commit.\n3. Run `git push origin <version_number>` to push the tag to GitHub.\n4. After merging your PR on GitHub, create a new release at https://github.com/drift-labs/driftpy/releases.\n   The CI process will upload a new version of the package to PyPI.\n',
    'author': 'Kevin Heavey',
    'author_email': 'kevinheavey123@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/drift-labs/driftpy',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

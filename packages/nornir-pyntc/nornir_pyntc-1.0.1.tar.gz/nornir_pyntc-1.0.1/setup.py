# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nornir_pyntc', 'nornir_pyntc.connections', 'nornir_pyntc.tasks']

package_data = \
{'': ['*']}

install_requires = \
['nornir>=3.2.0,<4.0.0', 'pyntc>=0.20.1,<0.21.0']

entry_points = \
{'console_scripts': ['nornir_pyntc = nornir_pyntc.cli:main'],
 'nornir.plugins.connections': ['pyntc = nornir_pyntc.connections:Pyntc']}

setup_kwargs = {
    'name': 'nornir-pyntc',
    'version': '1.0.1',
    'description': 'pyntc plugin for Nornir',
    'long_description': '# nornir-pyntc\n\n<p align="center">\n  <img src="https://raw.githubusercontent.com/networktocode/nornir-pyntc/develop/docs/images/nornir_pyntc_logo.png" class="logo" height="200px">\n  <br>\n  <a href="https://github.com/networktocode/nornir-pyntc/actions"><img src="https://github.com/networktocode/nornir-pyntc/actions/workflows/ci.yml/badge.svg?branch=main"></a>\n  <a href="https://nornir-pyntc.readthedocs.io/en/latest"><img src="https://readthedocs.org/projects/nornir-pyntc/badge/"></a>\n  <a href="https://pypi.org/project/nornir-pyntc/"><img src="https://img.shields.io/pypi/v/nornir-pyntc"></a>\n  <a href="https://pypi.org/project/nornir-pyntc/"><img src="https://img.shields.io/pypi/dm/nornir-pyntc"></a>\n  <br>\n</p>\n\n## Overview\n\nA pyntc plugin for Nornir.\n\n## Documentation\n\nFull web-based HTML documentation for this library can be found over on the [Nornir-Pyntc Docs](https://nornir-pyntc.readthedocs.io) website:\n\n- [User Guide](https://nornir-pyntc.readthedocs.io/en/latest/user/lib_overview/) - Overview, Using the library, Getting Started.\n- [Administrator Guide](https://nornir-pyntc.readthedocs.io/en/latest/admin/install/) - How to Install, Configure, Upgrade, or Uninstall the library.\n- [Developer Guide](https://nornir-pyntc.readthedocs.io/en/latest/dev/contributing/) - Extending the library, Code Reference, Contribution Guide.\n- [Release Notes / Changelog](https://nornir-pyntc.readthedocs.io/en/latest/admin/release_notes/).\n- [Frequently Asked Questions](https://nornir-pyntc.readthedocs.io/en/latest/user/faq/).\n\n### Contributing to the Docs\n\nAll the Markdown source for the library documentation can be found under the [docs](https://github.com/networktocode/nornir-pyntc/tree/develop/docs) folder in this repository. For simple edits, a Markdown capable editor is sufficient - clone the repository and edit away.\n\nIf you need to view the fully generated documentation site, you can build it with [mkdocs](https://www.mkdocs.org/). A container hosting the docs will be started using the invoke commands (details in the [Development Environment Guide](https://nornir-pyntc.readthedocs.io/en/latest/dev/dev_environment/#docker-development-environment)) on [http://localhost:8001](http://localhost:8001). As your changes are saved, the live docs will be automatically reloaded.\n\nAny PRs with fixes or improvements are very welcome!\n\n## Questions\n\nFor any questions or comments, please check the [FAQ](https://nornir-pyntc.readthedocs.io/en/latest/user/faq/) first. Feel free to also swing by the [Network to Code Slack](https://networktocode.slack.com/) (channel `#networktocode`), sign up [here](http://slack.networktocode.com/) if you don\'t have an account.\n',
    'author': 'Network to Code, LLC',
    'author_email': 'info@networktocode.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/networktocode-llc/nornir_pyntc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

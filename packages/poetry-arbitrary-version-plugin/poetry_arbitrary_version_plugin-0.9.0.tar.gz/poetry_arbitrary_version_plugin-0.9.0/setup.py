# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_arbitrary_version_plugin']

package_data = \
{'': ['*']}

install_requires = \
['poetry>=1.2.0a1']

entry_points = \
{'poetry.application.plugin': ['poetry-arbitrary-version-plugin = '
                               'poetry_arbitrary_version_plugin.plugin:ArbitraryVersionPlugin']}

setup_kwargs = {
    'name': 'poetry-arbitrary-version-plugin',
    'version': '0.9.0',
    'description': 'A Poetry plugin to override a version in a pyproject.toml from environment variable or build and publish command option',
    'long_description': '# Poetry Arbitrary Version Plugin\n\n[![CI](https://github.com/godfryd/poetry-arbitrary-version-plugin/actions/workflows/build.yml/badge.svg)](https://github.com/godfryd/poetry-arbitrary-version-plugin/actions/workflows/build.yml)\n\nA [Poetry](https://python-poetry.org/) plugin that allows a project\nbuilder to override the project version.  A project version can be\noverriden for example during CI process. The version can be overriden\nusing the environment variable `PROJECT_OVERRIDE_VERSION` or\nthe `--override-version` switch of the build command.\n\n## Install\n\nAdd the plugin to Poetry environment\n\n```sh\n$ poetry self add poetry-arbitrary-version-plugin\n```\n\nor install the plugin using `pip` to the place where `Poetry` is installed.\n\n```sh\n$ pip install poetry-arbitrary-version-plugin\n```\n\n## Usage\n\nOverriding a project version by `PROJECT_OVERRIDE_VERSION` environment variable:\n\n```console\n$ PROJECT_OVERRIDE_VERSION=3.2.1 poetry build -f sdist\nOverriden project version from 0.8.0 to 3.2.1\nBuilding poetry-arbitrary-version-plugin (3.2.1)\n  - Building sdist\n  - Built poetry_arbitrary_version_plugin-3.2.1.tar.gz\n```\n\nOverriding a project version by the `--override-version` switch:\n\n```console\n$ poetry build -f sdist --override-version=1.2.3\nOverriden project version from 0.8.0 to 1.2.3\nBuilding poetry-arbitrary-version-plugin (1.2.3)\n  - Building sdist\n  - Built poetry_arbitrary_version_plugin-1.2.3.tar.gz\n```\n',
    'author': 'Michal Nowikowski',
    'author_email': 'godfryd@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/godfryd/poetry-arbitrary-version-plugin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)

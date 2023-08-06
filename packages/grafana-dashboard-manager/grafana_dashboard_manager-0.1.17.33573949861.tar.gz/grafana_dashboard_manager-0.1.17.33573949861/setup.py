# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['grafana_dashboard_manager']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0',
 'rich>=10.14.0,<11.0.0',
 'six>=1.11.0,<2.0.0',
 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['grafana-dashboard-manager = '
                     'grafana_dashboard_manager.__main__:app']}

setup_kwargs = {
    'name': 'grafana-dashboard-manager',
    'version': '0.1.17.33573949861',
    'description': "A cli utility that uses Grafana's HTTP API to easily save and restore dashboards.",
    'long_description': '# grafana-dashboard-manager\n\n![CodeQL](https://github.com/Beam-Connectivity/grafana-dashboard-manager/actions/workflows/codeql-analysis.yml/badge.svg)\n\n## Introduction\n\nA simple CLI utility for importing or exporting dashboard JSON definitions using the Grafana HTTP API.\n\nThis can be used for:\n\n- Backing up your dashboards that already exist within your Grafana instance, e.g. if you are migrating from the internal SQLite database to MySQL.\n- Updating dashboard files for your Infrastructure-as-Code for use with [Grafana dashboard provisioning](https://grafana.com/docs/grafana/latest/administration/provisioning/#dashboards).\n- Making tweaks to dashboard JSON files directly and updating Grafana with one command.\n\n### Features\n\n- Mirrors the folder structure between a local set of dashboards and Grafana, creating folders where necessary.\n- Ensures links to dashboards folders in a `dashlist` Panel are consistent with the Folder IDs - useful for deploying one set of dashboards across multiple Grafana instances, for instance across environments.\n\n### Workflow\n\nThe intended workflow is:\n\n1. Create a dashboard and save it in the desired folder from within the Grafana web GUI\n2. Use `grafana-dashboard-manager` to extract the new dashboards and save them to a local directory or version control system.\n3. Dashboards can be created or updated from the local store and uploaded back into Grafana.\n\n## Installation\n\n### Install via _[pip](https://pypi.org/project/pip/)_:\n\n```shell\npip install grafana-dashboard-manager\n```\n\n### Install from source - requires _[Poetry](https://python-poetry.org/)_ on your system:\n\n```shell\ncd /path/to/grafana-dashboard-manager\npoetry install\n```\n\n## Usage\n\n### Credentials\n\nIt is important to note that the **admin** login username and password are required, and its selected organization must be correct, if you are accessing the API using `--username` and `--password`. Alternatively, the API Key must have **admin** permissions if you are accessing the API using `--token`.\n\nFor more help, see the full help text with `poetry run grafana-dashboard-manager --help`.\n\n### Download dashboards from web to solution-data using the Grafana admin user\n\n```shell\npoetry run grafana-dashboard-manager \\\n    --host https://my.grafana.com \\\n    --username admin_username --password admin_password \\\n    download all \\\n    --destination-dir /path/to/dashboards/\n```\n\n### Download dashboards from web to solution-data using a Grafana admin API Key\n\n```shell\npoetry run grafana-dashboard-manager \\\n    --host https://my.grafana.com \\\n    --token admin_api_key \\\n    download all \\\n    --destination-dir /path/to/dashboards/\n```\n\n### Upload dashboards from solution-data to web using the Grafana admin user\n\n```shell\npoetry run grafana-dashboard-manager \\\n    --host https://my.grafana.com \\\n    --username admin_username --password admin_password \\\n    upload all \\\n    --source-dir /path/to/dashboards/\n```\n\n### Upload dashboards from solution-data to web using a Grafana admin API Key\n\n```shell\npoetry run grafana-dashboard-manager \\\n    --host https://my.grafana.com \\\n    --token admin_api_key \\\n    upload all \\\n    --source-dir /path/to/dashboards/\n```\n\n**Please note:** if your Grafana is not hosted on port 80/443 as indicated by the protocol prefix, the port needs to be specified as part of the `--host` argument. For example, a locally hosted instance on port 3000: `--host http://localhost:3000`.\n\n## Limitations\n\n- The home dashboard new deployment needs the default home dashboard to be manually set in the web UI, as the API to set the organisation default dashboard seems to be broken, at least on v8.2.3.\n- Currently expects a hardcoded `home.json` dashboard to set as the home.\n- Does not handle upload of dashboards more deeply nested than Grafana supports.\n- Does not support multi-organization deployments.\n',
    'author': 'Vince Chan',
    'author_email': 'vince@beamconnectivity.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://www.beamconnectivity.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

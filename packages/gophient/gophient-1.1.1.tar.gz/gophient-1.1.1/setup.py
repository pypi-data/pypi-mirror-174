# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gophient']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'gophient',
    'version': '1.1.1',
    'description': 'Client library for the Gopherspace',
    'long_description': "# Gophient\n[![repo style: chr](https://img.shields.io/badge/repo%20style-chr-blueviolet?logo=github&style=flat)](https://github.com/arichr/python-template)\n[![PyPI](https://img.shields.io/pypi/v/gophient?style=flat&logo=python&logoColor=white)](https://pypi.org/project/gophient/)\n[![Maintainability](https://api.codeclimate.com/v1/badges/d83cf869ea9fa8d05a6f/maintainability)](https://codeclimate.com/github/arichr/gophient/maintainability)\n\nGophient is client library for the Gopherspace. It doesn't require any dependencies and is easy to use.\n\n**Features:**\n\n* Browse the Gopherspace\n* Follow links\n* Download content\n\n[![Read documentation](https://img.shields.io/badge/read-documentation-green?style=for-the-badge&logo=python&logoColor=white)](https://arichr.github.io/gophient/)\n\n## Examples\n### Get weather from Floodgap\n```python\nimport gophient\n\nclient = gophient.Gopher()\nweather = client.request('gopher.floodgap.com', 'groundhog/ws')\nprint(weather)\n```\n### Search by Veronica\n```python\nimport gophient\n\nclient = gophient.Gopher()\nresults = client.request('gopher.floodgap.com', 'v2/vs', query='plan 9')\nprint(results)\n```\n### Download files\n```python\nimport gophient\n\nclient = gophient.Gopher()\napk = client.request('gopher.floodgap.com', 'overbite/files/OverbiteAndroid025.apk')\nwith open('app.apk', 'wb') as apk_file:\n  apk_file.write(apk)\n```\n",
    'author': 'Arisu Wonderland',
    'author_email': 'arisuchr@riseup.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/arichr/gophient',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

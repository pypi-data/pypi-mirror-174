# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['myWebKraken_package']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mywebkraken-package',
    'version': '0.1.1',
    'description': '',
    'long_description': '# myWebKraken\nPRoyecto prueba que se conecta a Kraken,  descarga precios de kripro activos y los uestra en web\n\nPAra instalar:\n```\npip install -r requirements.txt\n```\n\nPara ejecutar\n\n```\nNo lo se todavia\n```',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

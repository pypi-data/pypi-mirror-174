# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pggm_datalab_utils']

package_data = \
{'': ['*']}

install_requires = \
['pyodbc>=4.0.34,<5.0.0']

setup_kwargs = {
    'name': 'pggm-datalab-utils',
    'version': '2.2',
    'description': 'Utilities created and used by the Datalab of PGGM',
    'long_description': '# Datalab utils\n\nWell-specified utilities from the Datalab of PGGM. Our aim with this package is to provide some tooling to make our lives a bit easier.\nSo far the package contains some database utilities, allowing you to connect to cloud databases using pyodbc in a standard pattern.',
    'author': 'Rik de Kort',
    'author_email': 'rik.de.kort@pggm.nl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

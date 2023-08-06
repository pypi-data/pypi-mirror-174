# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dicomautomaton']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dicomautomaton',
    'version': '0.1.0',
    'description': 'A multipurpose tool for analyzing medical physics data with a focus on automation.',
    'long_description': '# DICOMautomaton\n\nThis is a placeholder readme for the Python library for DICOMautomaton\n',
    'author': 'Hal Clark',
    'author_email': 'haley.clark@bccancer.bc.ca',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)

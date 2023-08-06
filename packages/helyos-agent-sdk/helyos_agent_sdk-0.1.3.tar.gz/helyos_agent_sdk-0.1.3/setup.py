# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['helyos_agent_sdk']

package_data = \
{'': ['*']}

install_requires = \
['dataclasses-json>=0.5.7,<0.6.0',
 'pika>=1.3.1,<2.0.0',
 'pycryptodome>=3.15.0,<4.0.0']

setup_kwargs = {
    'name': 'helyos-agent-sdk',
    'version': '0.1.3',
    'description': '',
    'long_description': '<div id="top"></div>\n\n<!-- PROJECT LOGO -->\n<br />\n<div align="center">\n  <a href="https://github.com/">\n    <img src="helyos_logo.png" alt="Logo"  height="80">\n    <img src="truck.png" alt="Logo"  height="80">\n  </a>\n\n  <h3 align="center">helyOS Agent SDK</h3>\n\n  <p align="center">\n    Methods and data strrctures to connect autonomous vehicles to helyOS.\n    <br />\n    <a href="https://fraunhoferivi.github.io/helyOS-agent-sdk/"><strong>Explore the docs »</strong></a>\n    <br />\n    <br />\n    <a href="https://github.com/">View Demo</a>\n    ·\n    <a href="https://github.com/FraunhoferIVI/helyOS-agent-sdk/issues">Report Bug</a>\n    ·\n    <a href="https://github.com/FraunhoferIVI/helyOS-agent-sdk/issues">Request Feature</a>\n  </p>\n</div>\n\n## About The Project\n\nThe helyos-agent-sdk python package encloses methods and data structures definitions that facilitate the connection to helyOS core through rabbitMQ.\n\n### List of features\n\n*   RabbitMQ client to communicate with helyOS. \n*   Check-in method.\n*   Agent and assignment status definitions. \n*   Easy access to helyOS assignments via callbacks. \n*   Application-level encryption.\n\n### Contributing\n\nKeep it simple. Keep it minimal.\n\n### Authors \n\n*   Carlos E. Viol Barbosa\n*   ...\n\n### License\n\nThis project is licensed under the MIT License',
    'author': 'Carlos Viol Barbosa',
    'author_email': 'you@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://helyos.ivi.fraunhofer.de',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

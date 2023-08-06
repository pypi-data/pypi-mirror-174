# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['engine', 'engine.cli', 'engine.connections']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'click>=8.1.3,<9.0.0',
 'tabulate>=0.9.0,<0.10.0',
 'yacs>=0.1.8,<0.2.0']

entry_points = \
{'console_scripts': ['engine = engine.cli:cli']}

setup_kwargs = {
    'name': 'granular-engine',
    'version': '0.1.0',
    'description': 'Experiment tracking for GeoSpatial Machine Learning on GeoEngine',
    'long_description': '===================\nEngine\n===================\n\nA Utility Library that assists in Geospatial Machine Learning Experiment Tracking.\n\nInstallation\n------------\n\n```pip install granular-engine```\n\n\nUsage\n-----\n\n>>> from engine import Engine\n>>>\n>>> # Make a config.yaml with GeoEngine projectId and exportId and other necessary details\n>>> engine = Engine("config.yaml")\n>>>\n>>> for epoch in enumerate(epochs):\n>>>   # train \n>>>   # eval\n>>>   engine.log(step=epoch, train_loss=train_loss, val_loss=val_loss)\n>>>\n>>> engine.done()\n\n\nLicense\n-------\nGPLv3\n\nDocumentation\n-------------\n\nView documentation `here <https://engine.granular.ai/>`_\n',
    'author': 'Sagar Verma',
    'author_email': 'sagar@granular.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/granularai/engine',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)

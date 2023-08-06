# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vsui', 'vsui.app', 'vsui.app.main']

package_data = \
{'': ['*'],
 'vsui': ['web/*',
          'web/public/*',
          'web/src/*',
          'web/src/components/*',
          'web/src/components/file_browser/*',
          'web/src/components/settings/*',
          'web/src/components/task/*',
          'web/src/stores/*',
          'web/tests/*'],
 'vsui.app': ['processes/VolumeSegmanticsPredict/*',
              'processes/VolumeSegmanticsTrain/*',
              'static/css/*',
              'static/fonts/*',
              'static/js/*',
              'templates/*']}

install_requires = \
['flask-socketio>=5.3.1,<6.0.0',
 'flask>=2.2.2,<3.0.0',
 'gevent-websocket>=0.10.1,<0.11.0',
 'gevent>=22.10.1,<23.0.0',
 'gunicorn>=20.1.0,<21.0.0',
 'pyyaml>=6.0,<7.0']

entry_points = \
{'console_scripts': ['vsui = vsui.vsui:main']}

setup_kwargs = {
    'name': 'vsui',
    'version': '0.1.0.4',
    'description': 'Flask server and vue frontend for monitoring the progress of a python script.',
    'long_description': '# Volume Segmantics User Interface',
    'author': 'Matthew Pimblott',
    'author_email': 'matthew.pimblott@diamond.ac.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

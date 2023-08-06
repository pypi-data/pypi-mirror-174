# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sys_tui', 'sys_tui.widgets']

package_data = \
{'': ['*'], 'sys_tui': ['renderables/*', 'views/*']}

install_requires = \
['psutil>=5.9.3,<6.0.0',
 'rich>=12.6.0,<13.0.0',
 'textual[dev]>=0.2.1,<0.3.0',
 'typer>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['sys_tui = sys_tui.main:app']}

setup_kwargs = {
    'name': 'sys-tui',
    'version': '0.1.0',
    'description': 'A textual app to monitor system utilities.',
    'long_description': '<h1 align="center">System TUI</h1>\n<p align="center">A textual app to monitor system utilities ⛽️</p>\n\n## Usage\n\n### Installation\n\n```bash\npipx install sys-tui\n```\n',
    'author': 'Luke Miloszewski',
    'author_email': 'lukemiloszewski@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/lukemiloszewski/sys-tui',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.0,<3.11.0',
}


setup(**setup_kwargs)

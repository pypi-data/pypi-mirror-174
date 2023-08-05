# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pycowsay_rich']

package_data = \
{'': ['*']}

install_requires = \
['rich>=11.0.0']

entry_points = \
{'console_scripts': ['pycowsay-rich = pycowsay_rich.talk:say'],
 'pipx.run': ['pycowsay-rich = pycowsay_rich.talk:say']}

setup_kwargs = {
    'name': 'pycowsay-rich',
    'version': '0.1.3',
    'description': 'A rich verion of pycowsay!',
    'long_description': '# pycowsay\n\nA talking cow! A rich version of [pycowsay](https://github.com/cs01/pycowsay).\n\n## Run\n\nUse [pipx](https://pypa.github.io/pipx/) to run without permanently installing\n\n```bash\npipx run pycowsay-rich mooo\n```\n\n## Install\n\nUse [pipx](https://pypa.github.io/pipx/) to install to isolated enviroment.\n\n```bash\npipx install pycowsay-rich\n```\n\nUse pip to install to python enviroment.\n\n```bash\npip install pycowsay-rich\n```\n\n',
    'author': 'Johannes Kaisinger',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://codeberg.org/KybernetikJo/pycowsay-rich',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

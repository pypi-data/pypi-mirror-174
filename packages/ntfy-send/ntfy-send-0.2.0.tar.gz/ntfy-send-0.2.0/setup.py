# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ns']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0', 'tomlkit>=0.11.6,<0.12.0']

entry_points = \
{'console_scripts': ['ntfy-send = ns.app:main']}

setup_kwargs = {
    'name': 'ntfy-send',
    'version': '0.2.0',
    'description': 'Client application for ntfy.sh',
    'long_description': '# ntfy-send\n\nntfy-send is a client application for notification service\n[ntfy.sh](https://ntfy.sh).\n\n## Configuration\n\nntfy-send can be configured via a configuration file. It is recommended\nmethod of storing your credential informations, which simplifies obtaining\nand sending them to ntfy server.\n\nAll configuration options can be enclosed in backticks (`). When this is the\ncase, the option is treated as a command whose output substitutes the\nconfigurration option.\n\nConfiguration files are stored in _$XDG_CONFIG_HOME/ntfy-send/config.toml_.\nIf you don\'t have _$XDG_CONFIG_HOME_ environment variale set, then it is\nstored in _~/.config/ntfy-send/config.toml_. Below are documented all\noptions:\n\n```toml\n# config.toml\n\n# URL to the server\nserver = "https://ntfy.sh"\n\n# Username and password can be automatically obtained each time they\'re\n# required. This is done by passing commands which should echo credentials.\n# For complex commands it\'s recommended to pot them in a separate script, due\n# to problems with several levels of quote escaping\n\n# Username and password can be passed in plain text. This isn\'t recommended.\nusername = "user"\npassword = "pass"\n\n# Alternatively, ntfy-send can automatically run a command for username and\n# password when they\'re enclosed in backticks (`):\nusername = """`gpg2 --decrypt pass.gpg | awk -F ":" \'/user:/ { printf $2 }\'`"""\npassword = """`gpg2 --decrypt pass.gpg | awk -F ":" \'/password:/ { printf $2 }\'`"""\n```\n\n',
    'author': 'Michal Goral',
    'author_email': 'dev@goral.net.pl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://git.goral.net.pl/mgoral/ntfy-send',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cipher_ey2335']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=7.2.0,<8.0.0']

setup_kwargs = {
    'name': 'cipher-ey2335',
    'version': '0.1.0',
    'description': 'A great package for hw07 by Ega Kurnia Yazid!',
    'long_description': '# cipher_ey2335\n\nA great package for hw07! It is the tool to encrypt and decrypt text using Caesar Cipher.\n\n## Installation\n\n```bash\n$ pip install cipher_ey2335\n```\n\n## Usage\n\n- TODO\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`cipher_ey2335` was created by Ega Kurnia Yazid. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`cipher_ey2335` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Ega Kurnia Yazid',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.1,<4.0.0',
}


setup(**setup_kwargs)

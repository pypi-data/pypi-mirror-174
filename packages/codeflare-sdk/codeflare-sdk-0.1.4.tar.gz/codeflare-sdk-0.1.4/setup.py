# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['codeflare_sdk', 'codeflare_sdk.cluster', 'codeflare_sdk.utils']

package_data = \
{'': ['*'], 'codeflare_sdk': ['templates/*']}

install_requires = \
['openshift-client==1.0.18', 'rich>=12.5,<13.0']

setup_kwargs = {
    'name': 'codeflare-sdk',
    'version': '0.1.4',
    'description': 'Python SDK for codeflare client',
    'long_description': '# Codeflare-SDK\n\nTo build the python package:\n - If poetry is not installed: `pip3 install poetry`\n - `poetry build`\n\nTo publish:\n - `poetry publish`\n',
    'author': 'Atin Sood',
    'author_email': 'asood@us.ibm.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/openshift-psap/codeflare-sdk',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

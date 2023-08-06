# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['my_tools', 'my_tools.tests']

package_data = \
{'': ['*']}

install_requires = \
['aenum>=3.1.11,<4.0.0',
 'auto-sklearn>=0.15.0,<0.16.0',
 'black[d]>=22.8.0,<23.0.0',
 'catboost>=1.1,<2.0',
 'einops>=0.4.1,<0.5.0',
 'gradio>=3.7,<4.0',
 'implicit>=0.6.1,<0.7.0',
 'jupyter-nbextensions-configurator>=0.5.0,<0.6.0',
 'jupyter>=1.0.0,<2.0.0',
 'matplotlib>=3.5.0,<3.6.0',
 'nb-black>=1.0.7,<2.0.0',
 'notebook==6.4.12',
 'numba>=0.56.2,<0.57.0',
 'numpy>=1.23.3,<2.0.0',
 'pandas>=1.5.0,<2.0.0',
 'protobuf==3.19.4',
 'pytest>=7.1.3,<8.0.0',
 'pytorch-lightning>=1.7.7,<2.0.0',
 'scipy>=1.9.1,<2.0.0',
 'shap>=0.41.0,<0.42.0',
 'sklearn>=0.0,<0.1',
 'transformers>=4.23.1,<5.0.0',
 'wandb>=0.13.3,<0.14.0']

extras_require = \
{':sys_platform == "darwin"': ['torch>=1.12.0,<2.0.0']}

setup_kwargs = {
    'name': 'ysda',
    'version': '0.1.0',
    'description': '',
    'long_description': '# YSDA\nYandex School of Data Analysis materials \n',
    'author': 'DimaKoshman',
    'author_email': 'koshmandk@yandex.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)

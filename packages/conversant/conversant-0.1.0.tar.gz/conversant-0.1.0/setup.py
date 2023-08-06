# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['conversant', 'conversant.prompts', 'conversant.search', 'conversant.utils']

package_data = \
{'': ['*'],
 'conversant': ['personas/client-support/*',
                'personas/fantasy-wizard/*',
                'personas/fortune-teller/*',
                'personas/injured-person/*',
                'personas/math-teacher/*',
                'personas/personal-trainer/*',
                'personas/watch-sales-agent/*']}

install_requires = \
['cohere>=2.8.0,<3.0.0',
 'emoji>=2.1.0,<3.0.0',
 'emojificate>=0.6.0,<0.7.0',
 'pydantic>=1.10.2,<2.0.0',
 'streamlit-ace>=0.1.1,<0.2.0',
 'streamlit-talk>=v0.0.3,<0.0.4',
 'toml>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'conversant',
    'version': '0.1.0',
    'description': 'Conversational AI tooling',
    'long_description': 'None',
    'author': 'Cohere ConvAI',
    'author_email': 'convai@cohere.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'libs'}

packages = \
['encord_active',
 'encord_active.common',
 'encord_active.embeddings',
 'encord_active.indexers',
 'encord_active.indexers.geometric',
 'encord_active.indexers.heuristic',
 'encord_active.indexers.semantic',
 'encord_active.model_predictions',
 'encord_active_app',
 'encord_active_app.common',
 'encord_active_app.common.components',
 'encord_active_app.common.components.sticky',
 'encord_active_app.conf',
 'encord_active_app.data_quality',
 'encord_active_app.data_quality.sub_pages',
 'encord_active_app.model_assertions',
 'encord_active_app.model_assertions.components',
 'encord_active_app.model_assertions.sub_pages',
 'encord_active_app.views']

package_data = \
{'': ['*'], 'encord_active_app': ['assets/*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'av>=9.2.0,<10.0.0',
 'encord>=0.1.43,<0.2.0',
 'faiss-cpu>=1.7.2,<2.0.0',
 'gdown>=4.5.1,<5.0.0',
 'inquirer>=2.10.0,<3.0.0',
 'loguru>=0.6.0,<0.7.0',
 'matplotlib>=3.5.3,<4.0.0',
 'natsort>=8.1.0,<9.0.0',
 'numpy>=1.23.1,<2.0.0',
 'opencv-python==4.5.5.64',
 'pandas>=1.4.3,<2.0.0',
 'plotly>=5.10.0,<6.0.0',
 'pycocotools>=2.0.5,<3.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'pytz>=2022.2.1,<2023.0.0',
 'rich>=12.6.0,<13.0.0',
 'scikit-learn>=1.0.1,<2.0.0',
 'scipy==1.8.1',
 'screeninfo>=0.8.1,<0.9.0',
 'shapely>=1.7.0,<2.0.0',
 'streamlit-modal>=0.0.5,<0.0.6',
 'streamlit-nested-layout>=0.1.1,<0.2.0',
 'streamlit==1.13.0',
 'termcolor>=2.0.1,<3.0.0',
 'torch>=1.12.1,<2.0.0',
 'torchvision>=0.13.1,<0.14.0',
 'typer>=0.6.1,<0.7.0',
 'types-pytz>=2022.2.1,<2023.0.0',
 'watchdog>=2.1.9,<3.0.0']

entry_points = \
{'console_scripts': ['encord-active = encord_active_app.main:cli']}

setup_kwargs = {
    'name': 'encord-active',
    'version': '0.1.6',
    'description': '',
    'long_description': None,
    'author': 'Frederik Hvilshøj',
    'author_email': 'frederik@cord.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9, !=2.7.*, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*, !=3.7.*, !=3.8.*',
}


setup(**setup_kwargs)

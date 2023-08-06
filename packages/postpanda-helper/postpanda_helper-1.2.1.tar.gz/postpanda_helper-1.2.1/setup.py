# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['postpanda_helper']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML',
 'SQLAlchemy>=1.3,<2.0',
 'logger-mixin>=1.1.0,<2.0.0',
 'numpy>=1.15,<2.0',
 'pandas>=1.1,<2.0',
 'pathvalidate>=2.3.2,<3.0.0']

extras_require = \
{':platform_python_implementation == "CPython"': ['psycopg2>=2.8,<3.0'],
 'geo': ['GeoAlchemy2>=0.8.4', 'geopandas>=0.9.0', 'shapely']}

setup_kwargs = {
    'name': 'postpanda-helper',
    'version': '1.2.1',
    'description': 'Various helpers for Postgres and Pandas, including SelectSert',
    'long_description': '# PostPanda Helper\n[![PyPI](https://img.shields.io/pypi/v/postpanda-helper?style=flat)](https://pypi.org/project/postpanda-helper/)\n[![PyPI - License](https://img.shields.io/pypi/l/postpanda-helper?style=flat)](https://pypi.org/project/postpanda-helper/)\n\nVarious helpers for PostgreSQL and Pandas\n\n[![Documentation](https://img.shields.io/static/v1?label=&message=Documentation&color=blue&style=for-the-badge&logo=Read+the+Docs&logoColor=white)](https://mumblepins.github.io/postpanda_helper/)',
    'author': 'Daniel Sullivan',
    'author_email': '4440652+mumblepins@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mumblepins/postpanda_helper',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

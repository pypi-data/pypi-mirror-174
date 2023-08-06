# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['juftin_scripts']

package_data = \
{'': ['*']}

install_requires = \
['art>=5.7,<6.0',
 'click>=8.1.2,<9.0.0',
 'pandas>=1.4',
 'rich-click>=1.5.2,<2.0.0',
 'rich>=12.6.0,<13.0.0',
 'textual>=0.3.0,<0.4.0']

extras_require = \
{'parquet': ['pyarrow>=9.0.0,<10.0.0']}

entry_points = \
{'console_scripts': ['juftin = juftin_scripts.__main__:cli']}

setup_kwargs = {
    'name': 'juftin-scripts',
    'version': '0.1.0',
    'description': 'Helpful Python scripts by @juftin',
    'long_description': '# juftin-scripts\n\nHelpful Python scripts by [@juftin](https://github.com/juftin)\n\n#### Check Out the [Docs](https://juftin.github.io/juftin-scripts/)\n\n___________\n___________\n\n<br/>\n\n<p align="center"><a href="https://github.com/juftin"><img src="https://raw.githubusercontent.com/juftin/juftin/main/static/juftin.png" width="120" height="120" alt="logo"></p>\n',
    'author': 'Justin Flannery',
    'author_email': 'juftin@juftin.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/juftin/juftin-scripts',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

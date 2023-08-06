# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['squaredown']

package_data = \
{'': ['*']}

install_requires = \
['aracnid-config>=1.0,<2.0',
 'aracnid-logger>=1.0,<2.0',
 'aracnid-utils>=1.0,<2.0',
 'i-mongodb>=1.0,<2.0',
 'squareup>=19.1,<20.0',
 'tqdm>=4.64,<5.0']

setup_kwargs = {
    'name': 'squaredown',
    'version': '1.2.1',
    'description': 'Customized Square interface',
    'long_description': '# Squaredown\n\nWe use Square as our point of sale system for our businesses. It works really well for most applications, but it takes too long to produce reports in a way that meets our business needs and the process is just too manual. We needed an automated way to produce our customized reports either at a click of a button or on a schedule. To do that we download the Square data into a MongoDB database. This is the code that we use to connect Square to MongoDB.\n\n## Getting Started\n\nThese instructions will get you a copy of the project up and running on your local machine for development and testing purposes.\n\n### Prerequisites\n\nThis package supports the following version of Python. It probably supports older versions, but they have not been tested.\n\n- Python 3.10 or later\n\n### Installing\n\nInstall the latest package using pip.\n\n```bash\n$ pip install squaredown\n```\n\nEnd with an example of getting some data out of the system or using it for a little demo\n\n## Running the tests\n\nExplain how to run the automated tests for this system\n\n```bash\n$ python -m pytest\n```\n\n## Usage\n\nTODO\n\n## Authors\n\n- **Jason Romano** - [Aracnid](https://github.com/aracnid)\n\nSee also the list of [contributors](https://github.com/lakeannebrewhouse/squaredown/contributors) who participated in this project.\n\n## License\n\nThis project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details\n',
    'author': 'Jason Romano',
    'author_email': 'aracnid@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/aracnid/squaredown',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

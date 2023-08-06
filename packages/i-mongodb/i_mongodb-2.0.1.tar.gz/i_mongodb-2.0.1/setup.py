# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['i_mongodb']

package_data = \
{'': ['*']}

install_requires = \
['aracnid_logger>=1.0,<2.0',
 'dnspython>=1.16,<2.0',
 'pymongo[srv]>=4.3,<5.0',
 'python-dateutil>=2.8,<3.0']

setup_kwargs = {
    'name': 'i-mongodb',
    'version': '2.0.1',
    'description': 'Customized connector to MongoDB',
    'long_description': '# i-MongoDB\n\nThis is a standardized and customized connector to MongoDB.\n\n## Getting Started\n\nThese instructions will get you a copy of the project up and running on your local machine for development and testing purposes.\n\n### Prerequisites\n\nThis package supports the following version of Python. It probably supports older versions, but they have not been tested.\n\n- Python 3.10 or later\n\n### Installing\n\nInstall the latest package using pip.\n\n```bash\n$ pip install i-mongodb\n```\n\nEnd with an example of getting some data out of the system or using it for a little demo\n\n## Running the tests\n\nExplain how to run the automated tests for this system\n\n```bash\n$ python -m pytest\n```\n\n## Usage\n\nTODO\n\n## Authors\n\n- **Jason Romano** - [Aracnid](https://github.com/aracnid)\n\nSee also the list of [contributors](https://github.com/aracnid/i-mongodb/contributors) who participated in this project.\n\n## License\n\nThis project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details\n',
    'author': 'Jason Romano',
    'author_email': 'aracnid@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/aracnid/i-mongodb',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

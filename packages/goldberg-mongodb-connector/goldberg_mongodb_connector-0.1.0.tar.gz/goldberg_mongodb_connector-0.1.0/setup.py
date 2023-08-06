# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mongodb_connector', 'mongodb_connector.connector', 'mongodb_connector.models']

package_data = \
{'': ['*']}

install_requires = \
['beanie>=1.13.1,<2.0.0']

setup_kwargs = {
    'name': 'goldberg-mongodb-connector',
    'version': '0.1.0',
    'description': '',
    'long_description': '# project-goldberg-mongodb\n\nThis repo should be used as connection to the MongoDB database for the Goldberg project.\n\n## Setup repository for development\n\n1. Create an environment with poetry\n\n    ```bash\n    poetry install\n    ```\n\n2. Create a `.env` file with the following content:\n\n    ```bash\n    MONGO_URI=mongodb://localhost:27017\n    MONGO_DB=goldberg\n    ```\n\n3. Run the tests\n\n    ```bash\n    poetry run pytest\n    ```\n',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

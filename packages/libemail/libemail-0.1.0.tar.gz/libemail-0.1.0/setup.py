# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['libemail']

package_data = \
{'': ['*'], 'libemail': ['templates/libemail/*']}

install_requires = \
['django>=3.0,<=5.0']

setup_kwargs = {
    'name': 'libemail',
    'version': '0.1.0',
    'description': 'Thin wrapper for Django EmailMessage',
    'long_description': '# libemail\n\n## Installation\n\n1. Install the app\n    \n    ```\n    pip install libemail\n    ```\n\n2. Add `libemail` to `INSTALLED_APPS` in `settings.py` file\n\n## Usage:\n\n1. Build the template context\n\n    ```\n    from libemail.generic import Email, EmailContext\n\n\n    email_context = EmailContext(\n        title="A simple title",\n        subtitle="A descriptive subtitle",\n        body="A long enough body, very detailed",\n        preview="Preview text that will be displayed on the list view of the mail client",\n        branding="A link to a image, white or transparent background",\n    )\n    ```\n\n2. Initialize an email object\n\n    ```\n    email = Email(subject="A very serious subject", context=email_context, to="some@email.com")\n    ```\n\n3. Send it!\n\n    ```\n    email.send()\n    ```\n\n',
    'author': 'Eglenelid Gamaliel Gutierrez Hernandez',
    'author_email': 'eglenelid.gamaliel@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['api_reflector',
 'api_reflector.migrations',
 'api_reflector.migrations.versions']

package_data = \
{'': ['*'], 'api_reflector': ['static/*', 'templates/*', 'templates/admin/*']}

modules = \
['settings']
install_requires = \
['Flask-Admin>=1.6.0,<2.0.0',
 'Flask-Cors>=3.0.10,<4.0.0',
 'Flask-Dance>=6.1.1,<7.0.0',
 'Flask-SQLAlchemy>=2.5.1,<3.0.0',
 'Flask>=2.2.2,<3.0.0',
 'Jinja2>=3.1.2,<4.0.0',
 'alembic>=1.8.1,<2.0.0',
 'blinker>=1.5,<2.0',
 'cachetools>=5.2.0,<6.0.0',
 'fasteners>=0.18,<0.19',
 'gunicorn>=20.1.0,<21.0.0',
 'pendulum>=2.1.2,<3.0.0',
 'psycopg2-binary>=2.9.3,<3.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'python-slugify>=6.1.2,<7.0.0',
 'sentry-sdk>=1.9.9,<2.0.0',
 'wtforms==2.3.3']

entry_points = \
{'console_scripts': ['api-reflector-migrate = '
                     'api_reflector.migrations.run_migrations:main']}

setup_kwargs = {
    'name': 'api-reflector',
    'version': '0.6.2',
    'description': 'A configurable API mocking service',
    'long_description': 'None',
    'author': 'Chris Latham',
    'author_email': 'cl@bink.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

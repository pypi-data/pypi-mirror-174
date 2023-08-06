# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kraken',
 'kraken.migrations',
 'kraken.migrations.versions',
 'kraken.server',
 'kraken.server.bg',
 'kraken.server.cloud']

package_data = \
{'': ['*']}

install_requires = \
['Authlib>=1.1.0,<2.0.0',
 'Flask-SQLAlchemy>=2.5.1,<3.0.0',
 'Flask>=1.1.4,<2.0.0',
 'MarkupSafe==2.0.1',
 'RestrictedPython==5.0',
 'SQLAlchemy>=1.4.25,<2.0.0',
 'alembic>=1.7.3,<2.0.0',
 'apscheduler>=3.8.0,<4.0.0',
 'azure-identity>=1.6.1,<2.0.0',
 'azure-mgmt-compute>=23.0.0,<24.0.0',
 'azure-mgmt-monitor>=2.0.0,<3.0.0',
 'azure-mgmt-network>=19.0.0,<20.0.0',
 'azure-mgmt-resource>=19.0.0,<20.0.0',
 'azure-mgmt-storage>=18.0.0,<19.0.0',
 'azure-mgmt-subscription>=1.0.0,<2.0.0',
 'boto3>=1.18.52,<2.0.0',
 'casbin>=1.17.1,<2.0.0',
 'clickhouse-driver>=0.2.2,<0.3.0',
 'connexion>=2.13.1,<3.0.0',
 'giturlparse>=0.10.0,<0.11.0',
 'gunicorn>=20.1.0,<21.0.0',
 'jsonschema>=4.5.0,<5.0.0',
 'kubernetes>=20.13.0,<21.0.0',
 'minio>=7.1.0,<8.0.0',
 'passlib>=1.7.4,<2.0.0',
 'psycopg2-binary>=2.9.1,<3.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'python-ldap>=3.4.3,<4.0.0',
 'pytimeparse>=1.1.8,<2.0.0',
 'redis>=3.5.3,<4.0.0',
 'requests>=2.26.0,<3.0.0',
 'rq>=1.10.0,<2.0.0',
 'sentry-sdk[flask]>=1.5.0,<2.0.0',
 'swagger-ui-bundle>=0.0.9,<0.0.10',
 'tzlocal==2.1']

entry_points = \
{'console_scripts': ['kkdbmigrate = kraken.migrations.apply:main',
                     'kkplanner = kraken.server.planner:main',
                     'kkqneck = kraken.server.qneck:main',
                     'kkrq = kraken.server.kkrq:main',
                     'kkscheduler = kraken.server.scheduler:main',
                     'kkwatchdog = kraken.server.watchdog:main']}

setup_kwargs = {
    'name': 'krakenci-server',
    'version': '0.1047',
    'description': 'Kraken CI server.',
    'long_description': 'None',
    'author': 'Michal Nowikowski',
    'author_email': 'godfryd@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://kraken.ci/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

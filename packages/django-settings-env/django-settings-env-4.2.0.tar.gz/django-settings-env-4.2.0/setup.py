# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_settings_env']

package_data = \
{'': ['*']}

install_requires = \
['Django>3.2', 'envex>1.2', 'python-dotenv>=0.21.0,<0.22.0']

extras_require = \
{'django-class-settings': ['django-class-settings>=0.2,<0.3']}

setup_kwargs = {
    'name': 'django-settings-env',
    'version': '4.2.0',
    'description': '12-factor.net settings support for Django based on envex',
    'long_description': '-------------------\ndjango-settings-env\n-------------------\n12-factor.net settings environment handler for Django\n\nenvex\n---------\n\nThe functionality outlined in this section is derived from the dependent package\n`envex`, the docs for which are partially repeated below.\n\nSkip to the Django Support section for functionality added by this extension.\n\n`envex` provides a convenient type-smart interface for handling the environment, and therefore\nconfiguration of any application using 12factor.net principals removing many environment specific\nvariables and security sensitive information from application code.\n\nThis module provides some features not supported by other dotenv handlers\n(python-dotenv, etc.) including expansion of template variables which is very useful\nfor DRY.\n\nMore detailed info can be found in the `envex` README.\n\n\nDjango Support\n--------------\n\nBy default, the Env class provided by this module can apply a given prefix (default "DJANGO_")\nto environment variables names, but will only be used in that form if the raw (unprefixed)\nvariable name is not set in the environment. To change the prefix including setting it to\nan empty string, pass the prefix= kwarg to `Env.__init__`.\n\nSome django specific methods included in this module are URL parsers for:\n\n| Default Var    | Parser\n|----------------|----------------------- \n| DATABASE_URL   | `env.database_url()`\n| CACHE_URL      | `env.cache_url()`\n| EMAIL_URL      | `env.email_url()`\n| SEARCH_URL     | `env.search_url()`\n| QUEUE_URL      | `env.queue_url()`\n\neach of which can be injected into django settings via the environment, typically\nfrom a .env file at the project root.\n\nThe name of the file and paths searched is fully customisable.\n\nThe url specified includes a schema that determines the "backend" class or module\nthat handles the corresponding functionality as documented below.\n\n## `database_url`\nEvaluates a URL in the form \n```\nschema://[username:[password]@]host_or_path[:port]/name\n```\nSchemas:\n\n| Scheme          | Database\n|-----------------|----------------------\n| postgres        | Postgres (psycopg2)\n| postgresql      | Postgres (psycopg2)\n| psql            | Postgres (psycopg2)\n| pgsql           | Postgres (psycopg2)\n| postgis         | Postgres (psycopg2) using PostGIS extensions\n| mysql           | MySql (mysqlclient) \n| mysql2          | MySql (mysqlclient)\n| mysql-connector | MySql (mysql-connector)\n| mysqlgis        | MySql (mysqlclient) using GIS extensions\n| mssql           | SqlServer (sql_server.pyodbc)\n| oracle          | Oracle (cx_Oracle)\n| pyodbc          | ODBC (pyodbc)\n| redshift        | Amazon Redshift\n| spatialite      | Sqlite with spatial extensions (spatialite)\n| sqlite          | Sqlite\n| ldap            | django-ldap\n\n## `cache_url`\nEvaluates a URL in the form\n```\nschema://[username:[password]@]host_or_path[:port]/[name]\n```\nSchemas:\n\n| Scheme          | Cache\n|-----------------|----------------------\n| dbcache         | cache in database\n| dummycache      | dummy cache - "no cache" \n| filecache       | cache data in files\n| locmemcache     | cache in memory\n| memcache        | memcached (python-memcached)\n| pymemcache      | memcached (pymemcache)\n| rediscache      | redis (django-redis)\n| redis           | redis (django-redis)\n\n## `email_url`\nEvaluates a URL in the form\n```\nschema://[username[@domain]:[password]@]host_or_path[:port]/\n```\nSchemas:\n\n| Scheme          | Service\n|-----------------|----------------------\n| smtp            | smtp, no SSL\n| smtps           | smtp over SSL\n| smtp+tls        | smtp over SSL\n| smtp+ssl        | smtp over SSL\n| consolemail     | publish mail to console (dev)\n| filemail        | append email to file (dev)\n| memorymail      | store emails in memory\n| dummymail       | do-nothing email backend\n| amazonses       | Amazon Wimple Email Service\n| amazon-ses      | Amazon Wimple Email Service\n\n## `search_url`\nEvaluates a URL in the form\n```\nschema://[username:[password]@]host_or_path[:port]/[index]\n```\nSchemas:\n\n| Scheme          | Engine\n|-----------------|----------------------\n| elasticsearch   | elasticsearch (django-haystack)\n| elasticsearch2  | elasticsearch2 (django-haystack)\n| solr            | Apache solr (django-haystack)\n| whoosh          | Whoosh search engine (pure python, haystack)\n| xapian          | Xapian search engine (haystack)\n| simple          | Simple search engine (haystack)\n\n## `queue_url`\nEvaluates a URL in the form\n```\nschema://[username:[password]@]host_or_path[:port]/[queue]\n```\nSchemas:\n\n| Scheme          | Engine\n|-----------------|----------------------\n| rabbitmq        | RabbitMQ\n| redis           | Redis\n| amazonsqs       | Amazon SQS\n| amazon-sqs      | alias for Amazon SQS\n\n\nDjango Class Settings\n---------------------\n\nSupport for the `django-class-settings` module is added to the env handler, allowing\na much simplified use withing a class_settings.Settings class, e.g.:\n\n```python\nfrom django_settings_env import Env\nfrom class_settings import Settings\n\nenv = Env(prefix=\'DJANGO_\')\n\nclass MySettings(Settings):\n    MYSETTING = env()\n```\nThis usage will look for \'MYSETTING\' or \'DJANGO_MYSETTNG\' in the environment and lazily\nassign it to the MYSETTING value for the settings class.\n\n> :warning: The functional form of env() is now available even if django class settings is not\nused or installed.\n\n',
    'author': 'David Nugent',
    'author_email': 'davidn@uniquode.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

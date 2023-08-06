# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysdbapi', 'pysdbapi.type_hints']

package_data = \
{'': ['*']}

extras_require = \
{'pretty': ['prettytable>=3.5.0,<4.0.0']}

setup_kwargs = {
    'name': 'pysdbapi',
    'version': '0.5.0',
    'description': 'pySDBAPI - simple database API. Use a couple of lines to make a request',
    'long_description': '# pysdbapi\n\n[![Dependencies](https://img.shields.io/librariesio/github/axemanofic/pysdbapi)](https://pypi.org/project/pysdbapi/)\n[![Version](https://img.shields.io/pypi/v/pysdbapi?color=green)](https://pypi.org/project/pysdbapi/)\n[![Downloads](https://pepy.tech/badge/pysdbapi/month)](https://pepy.tech/project/pysdbapi)\n[![Downloads](https://pepy.tech/badge/pysdbapi/week)](https://pepy.tech/project/pysdbapi)\n\npySDBAPI - simple database API. Use a couple of lines to make a request\n\n## Features\n\n* Use a single decorator to complete a request. Receive OrderedDict immediately in response.\n* If you need to display the table in the console, then use the __show_table__ parameter\n* So far only SQLite is supported, support for other databases (MySQL, PostgreSQL and others) will be added in the future\n\n## Installation\n\n```text\npoetry add pysdbapi\n```\n\nor\n\n```text\npip install pysdbapi\n```\n\n### Optional dependencies\n\nThis dependency is needed to print the table to the console\n\n```text\npoetry add pysdbapi[pretty]\n```\n\n## Example SQLite\n\nThis code sends a message on your behalf to the chat\n\n```python\nimport pysdbapi\n\nDATABASE_SETTINGS = {"database": "test.db"}\n\ndb = pysdbapi.DBApi(DATABASE_SETTINGS)\n\n@db.execute_sql()\ndef get_all_posts():\n    return """SELECT * FROM posts"""\n\n\n@db.execute_sql(show_table=True)\ndef get_all_posts__table():\n    return """SELECT * FROM posts"""\n```\n\nResult:\n\n```\n# Example show table\n\n+----+-----------+----------------------+\n| id |   title   |         text         |\n+----+-----------+----------------------+\n| 1  | Article 1 | Some text in article |\n| 2  | Article 2 | Some text in article |\n| 3  | Article 3 | Some text in article |\n| 4  | Article 4 | Some text in article |\n| 5  | Article 5 | Some text in article |\n| 6  |   dasdas  |       sddsdas        |\n+----+-----------+----------------------+\n```\n',
    'author': 'Roman',
    'author_email': 'axeman.ofic@gmail.com',
    'maintainer': 'Roman',
    'maintainer_email': 'axeman.ofic@gmail.com',
    'url': 'https://github.com/axemanofic/pysdbapi',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

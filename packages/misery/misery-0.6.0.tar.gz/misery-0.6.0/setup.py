# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['misery']

package_data = \
{'': ['*']}

install_requires = \
['ipaddress>=1.0.23,<2.0.0']

extras_require = \
{'clickhouse': ['PyPika>=0.48.9,<0.49.0', 'aiohttp>=3.8.1,<4.0.0'],
 'postgres': ['PyPika>=0.48.9,<0.49.0', 'asyncpg>=0.25.0,<0.26.0']}

setup_kwargs = {
    'name': 'misery',
    'version': '0.6.0',
    'description': 'asyncio-friendly database toolkit',
    'long_description': '<p align="center">\n    <img src="https://github.com/meowmeowcode/misery/blob/clickhouse/docs/source/_static/misery.png" width="200" alt="misery" />\n</p>\n\n\n# Misery\n\nAn **asyncio**-friendly database toolkit that works well with **MyPy**.\n\n## Supported database systems\n\nAt the moment, PostgreSQL and ClickHouse are supported.\n\n## Documentation\n\nThe latest documentation: https://misery.readthedocs.io\n\n## Usage example\n\n```python\nfrom dataclasses import dataclass\nfrom uuid import UUID, uuid4\n\nimport asyncpg\nfrom pypika import Table\nfrom misery.postgres import PostgresRepo\n\n\nconn = await asyncpg.connect("postgresql://postgres:password@localhost/postgres")\n\nawait conn.execute(\n    """\n        CREATE TABLE users (\n            id uuid PRIMARY KEY,\n            name text NOT NULL UNIQUE\n        );\n    """\n)\n\n\n@dataclass\nclass User:\n    id: UUID\n    name: str\n\n\nclass UsersRepo(PostgresRepo[User]):\n    table = Table("users")\n\n\nusers_repo = UsersRepo(conn)\n\nuser_id = uuid4()\nbob = User(id=user_id, name="Bob")\nawait users_repo.add(bob)\n\nuser = await users_repo.get(id=user_id)\nassert user == bob\n```',
    'author': 'Anton Evdokimov',
    'author_email': 'meowmeowcode@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)

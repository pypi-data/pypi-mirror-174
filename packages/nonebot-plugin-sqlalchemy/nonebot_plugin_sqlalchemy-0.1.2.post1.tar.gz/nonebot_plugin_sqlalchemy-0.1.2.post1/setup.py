# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nonebot_plugin_sqlalchemy']

package_data = \
{'': ['*']}

install_requires = \
['nonebot2>=2.0.0-rc.1,<3.0.0', 'sqlalchemy[asyncio]>=1.4.42,<2.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-sqlalchemy',
    'version': '0.1.2.post1',
    'description': '',
    'long_description': 'nonebot-plugin-sqlalchemy\n==========\n\n为nonebot2提供简单的sqlalchemy封装\n\n## Get Started\n\n```python\n# 【1】定义data_source\nfrom nonebot import get_driver, require\n\n# 注意必须先require再import\nrequire("nonebot_plugin_sqlalchemy")\nfrom nonebot_plugin_sqlalchemy import DataSource\n\n# 必须使用支持asyncio的驱动器\ndb_conn_url = "postgresql+asyncpg://username:password@localhost:5432/database"\ndata_source = DataSource(get_driver(), db_conn_url)\n\n\n# 【2】定义映射\nfrom sqlalchemy import Column, String, BigInteger, Integer\n\n@data_source.registry.mapped\nclass UserOrm:\n    __tablename__ = \'users\'\n\n    id: int = Column(Integer, primary_key=True, autoincrement=True)\n    username: str = Column(String)\n    password: str = Column(String)\n    nickname: str = Column(String)\n\n    \n# 【3】在nonebot中使用\nfrom nonebot import on_command\nfrom nonebot.adapters.onebot.v11 import MessageEvent\nfrom nonebot.internal.matcher import Matcher\nfrom sqlalchemy import select\n\nlogin_matcher = on_command("login")\n\n@login_matcher.handle()\nasync def handler(event: MessageEvent, matcher: Matcher):\n    username, password = event.get_plaintext().split(" ")\n    \n    session = data_source.session()\n    \n    stmt = select(UserOrm).where(UserOrm.username == username, UserOrm.password == password)\n    result = await session.execute(stmt)\n    user = result.scalar_one_or_none()\n\n    if user is not None:\n        await matcher.send(f"Hello, {user.nickname}")\n```\n',
    'author': 'ssttkkl',
    'author_email': 'huang.wen.long@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ssttkkl/nonebot-plugin-sqlalchemy',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

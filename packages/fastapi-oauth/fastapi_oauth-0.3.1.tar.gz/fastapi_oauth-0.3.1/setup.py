# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['fastapi_oauth',
 'fastapi_oauth.common',
 'fastapi_oauth.rfc6749',
 'fastapi_oauth.rfc6749.grants',
 'fastapi_oauth.rfc6750',
 'fastapi_oauth.rfc7009',
 'fastapi_oauth.rfc7636',
 'fastapi_oauth.utils']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy[asyncio]>=1.4.28,<2.0.0',
 'Werkzeug>=2.2.2,<3.0.0',
 'fastapi>=0.85.1,<0.86.0',
 'pydantic[dotenv]>=1.10.2,<2.0.0']

setup_kwargs = {
    'name': 'fastapi-oauth',
    'version': '0.3.1',
    'description': 'OAuth2 Provider in FastAPI',
    'long_description': 'None',
    'author': 'Đỗ Quốc Vương',
    'author_email': 'vuongtlt13@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

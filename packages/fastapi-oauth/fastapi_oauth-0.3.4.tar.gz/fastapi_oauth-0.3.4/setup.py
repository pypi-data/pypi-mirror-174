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
    'version': '0.3.4',
    'description': 'OAuth2 Provider in FastAPI',
    'long_description': 'FastAPI-OAuth\n==============\n\n[![Stable Version](https://img.shields.io/pypi/v/fastapi-oauth?color=blue)](https://pypi.org/project/fastapi-oauth/)\n[![Downloads](https://img.shields.io/pypi/dm/fastapi-oauth)](https://pypistats.org/packages/fastapi-oauth)\n[![Build Status](https://github.com/vuongtlt13/fastapi-oauth/actions/workflows/build.yml/badge.svg)](https://github.com/vuongtlt13/fastapi-oauth/actions)\n[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)\n\nFastAPI OAuth2 Provider\n\nProvider Example: https://github.com/vuongtlt13/example_fastapi_oauth_provider\n',
    'author': 'Đỗ Quốc Vương',
    'author_email': 'vuongtlt13@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/vuongtlt13/fastapi-oauth',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

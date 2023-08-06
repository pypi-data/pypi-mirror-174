# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['memofn', 'memofn.utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'memofn',
    'version': '0.1.0',
    'description': 'A python library for memoizing functions for quick debugging/translations',
    'long_description': "# MemoFN\n\nA python library for memoizing functions for quick debugging/translations.\n\n## Usage\n\n```python\nfrom memofn import memofn, load_cache, save_cache\n\ndef fib(n):\n    if n < 2:\n        return n\n    return fib(n-1) + fib(n-2)\n\nload_cache('fib.cache.pkl')\nmfib = memofn(expire_in_days=9)(fib)\nmfib(10)\nsave_cache('fib.cache.pkl')\n```\n",
    'author': 'Moises Baltazar',
    'author_email': 'null@moisesb.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

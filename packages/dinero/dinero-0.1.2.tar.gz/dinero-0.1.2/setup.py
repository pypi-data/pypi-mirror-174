# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dinero', 'dinero.currencies']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dinero',
    'version': '0.1.2',
    'description': 'Dinero is a library for working with monetary values in Python.',
    'long_description': '<p align="center">\n  <img width="300" height="200" src="https://media.tenor.com/EWRvErYGzPUAAAAC/bugs-bunny-looney-tunes.gif">\n</p>\n\n<h1 align="center">Dinero</h1>\n\nA Dinero object is an immutable data structure representing a specific monetary value. It comes with methods for creating, parsing, manipulating, testing and formatting them.\n\n[Documentation (WIP)](https://wilfredinni.github.io/dinero/)\n\n## Install\n\nDinero is a dependency free project.\n\n```bash\npip install dinero\n```\n\n## The problem\n\n> Using floats to do exact calculations in Python can be dangerous. When you try to find out how much 2.32 x 3 is, Python tells you it\'s 6.959999999999999. For some calculations, that’s fine. But if you are calculating a transaction involving money, that’s not what you want to see. Sure, you could round it off, but that\'s a little hacky.\n\n```python\n>>> 2.32 * 3 == 6.96\nFalse\n>>> 2.32 * 3\n6.959999999999999\n```\n\nYou can read [How to Count Money Exactly in Python](https://learnpython.com/blog/count-money-python/) to get a better idea.\n\n## Why Dinero?\n\nPython `Decimal` instances are enough for basic cases but when you face more complex use-cases they often show limitations and are not so intuitive to work with. Dinero provides a cleaner and more easy to use API while still relying on the standard library. So it\'s still `Decimal` but easier.\n\n```python\n>>> from dinero import Dinero\n>>> from dinero.currencies import USD\n>>>\n>>> Dinero(2.32, USD) * 3 == 6.96\nTrue\n```\n\nDinero give you access to more than 100 different currencies:\n\n```python\n>>> from dinero import Dinero\n>>> from dinero.currencies import USD, EUR, GBP, INR, CLP\n```\n\n```python\n>>> Dinero(2.32, EUR)\nDinero(amount=2.32, currency={\'code\': \'EUR\', \'base\': 10, \'exponent\': 2, \'symbol\': \'€\'})\n```\n\n```python\n>>> Dinero(2.32, EUR).format(symbol=True, currency=True)\n\'€2.32 EUR\'\n```\n\n```python\n>>> Dinero(2.32, EUR).raw_amount\nDecimal(\'2.32\')\n```\n\nYou can perform operations:\n\n```python\n>>> total = Dinero(456.343567, USD) + 345.32 *  3\n>>> print(total)\n# 1,492.30\n```\n\n```python\n>>> product = Dinero(345.32, USD).multiply(3)\n>>> total = product.add(456.343567)\n>>> print(total)\n# 1,492.30\n```\n\nAnd comparisons:\n\n```python\n>>> Dinero(100, EUR) == Dinero(100, EUR)\nTrue\n>>> Dinero(100, EUR) < Dinero(100, EUR)\nFalse\n>>> Dinero(100, EUR) <= Dinero(100, EUR)\nTrue\n>>> Dinero(100, EUR) > Dinero(100, EUR)\nFalse\n>>> Dinero(100, EUR) >= Dinero(100, EUR)\nTrue\n```\n',
    'author': 'Carlos Montecinos Geisse',
    'author_email': 'carlos@pythoncheatsheet.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/wilfredinni/dinero',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

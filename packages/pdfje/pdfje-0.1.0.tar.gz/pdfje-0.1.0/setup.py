# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pdfje']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1,<5']}

setup_kwargs = {
    'name': 'pdfje',
    'version': '0.1.0',
    'description': 'Tiny PDF writer',
    'long_description': '🖍 PDFje\n========\n\n.. image:: https://img.shields.io/pypi/v/pdfje.svg?style=flat-square\n   :target: https://pypi.python.org/pypi/pdfje\n\n.. image:: https://img.shields.io/pypi/l/pdfje.svg?style=flat-square\n   :target: https://pypi.python.org/pypi/pdfje\n\n.. image:: https://img.shields.io/pypi/pyversions/pdfje.svg?style=flat-square\n   :target: https://pypi.python.org/pypi/pdfje\n\n.. image:: https://img.shields.io/readthedocs/pdfje.svg?style=flat-square\n   :target: http://pdfje.readthedocs.io/\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square\n   :target: https://github.com/psf/black\n\n-----\n\n  **PDF·je** *(noun)* Dutch for \'small PDF\'\n\nTiny library for writing simple PDFs. Experimental.\n\nCurrently under development.\nLeave a ⭐️ on GitHub if you\'re interested how this develops!\n\nWhy?\n----\n\nThe most popular libraries for writing PDFs are quite old and inspired by Java and PHP.\n*PDFje* aims to be a modern, Pythonic library with a more declarative API.\n\nHow does it work?\n-----------------\n\n.. code-block:: python\n\n  >>> from pdfje import Document, Page, Text\n  >>> pdf.Document([\n  ...     Page([Text("Hello", at=(200, 700)), Text("World", at=(300, 670))]),\n  ...     Page(),\n  ...     Page([Text("This is the last page!", at=(300, 600))]),\n  ...\n  ... ]).to_path(\'hello.pdf\')\n\nSee `the docs <https://pdfje.rtfd.io>`_ for a complete overview.\n\nInstallation\n------------\n\nIt\'s available on PyPI.\n\n.. code-block:: bash\n\n  pip install pdfje\n',
    'author': 'Arie Bovenberg',
    'author_email': 'a.c.bovenberg@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ariebovenberg/pdfje',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

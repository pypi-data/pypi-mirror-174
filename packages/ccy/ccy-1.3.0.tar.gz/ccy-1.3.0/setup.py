# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ccy', 'ccy.core', 'ccy.dates', 'ccy.tradingcentres']

package_data = \
{'': ['*']}

install_requires = \
['python-dateutil>=2.8.2,<3.0.0', 'pytz>=2022.5,<2023.0']

setup_kwargs = {
    'name': 'ccy',
    'version': '1.3.0',
    'description': 'Python currencies',
    'long_description': "A python module for currencies. The module compiles a dictionary of\ncurrency objects containing information useful in financial analysis.\nNot all currencies in the world are supported yet. You are welcome to\njoin and add more.\n\n:Package: |version| |license| |pyversions| |status| |downloads|\n:CI: |master-build| |coverage-master|\n:Dowloads: https://pypi.org/project/ccy/\n:Source: https://github.com/quantmind/ccy\n\n.. |version| image:: https://badge.fury.io/py/ccy.svg\n  :target: https://badge.fury.io/py/ccy\n.. |pyversions| image:: https://img.shields.io/pypi/pyversions/ccy.svg\n  :target: https://pypi.org/project/ccy/\n.. |license| image:: https://img.shields.io/pypi/l/ccy.svg\n  :target: https://pypi.org/project/ccy/\n.. |status| image:: https://img.shields.io/pypi/status/ccy.svg\n  :target: https://pypi.org/project/ccy/\n.. |downloads| image:: https://img.shields.io/pypi/dd/ccy.svg\n  :target: https://pypi.org/project/ccy/\n.. |master-build| image:: https://github.com/quantmind/ccy/workflows/build/badge.svg\n  :target: https://github.com/quantmind/ccy/actions?query=workflow%3Abuild\n.. |coverage-master| image:: https://codecov.io/gh/quantmind/ccy/branch/master/graph/badge.svg\n  :target: https://codecov.io/gh/quantmind/ccy\n\n\n.. contents::\n    :local:\n\n\nCurrency object\n======================\nTo use it::\n\n    >>> import ccy\n    >>> c = ccy.currency('aud')\n    >>> c.printinfo()\n    code: AUD\n    twoletterscode: AD\n    rounding: 4\n    default_country: AU\n    isonumber: 036\n    order: 3\n    name: Australian Dollar\n    >>> c.as_cross()\n    'AUDUSD'\n    >>> c.as_cross('/')\n    'AUD/USD'\n\na currency object has the following properties:\n\n* *code*: the `ISO 4217`_ code.\n* *twoletterscode*: two letter code (can't remeber the ISO number). Very useful for financial data providers such as Bloomberg.\n* *default_country*: the default `ISO 3166-1 alpha-2`_ country code for the currency.\n* *isonumber*: the ISO 4217 number.\n* *name*: the name of the currency.\n* *order*: default ordering in currency pairs (more of this below).\n* *rounding*: number of decimal places\n\nCurrency Crosses\n~~~~~~~~~~~~~~~~~~~~~~~~~~\n\nYou can create currency pairs by using the ``currency_pair`` function::\n\n    >>> import ccy\n    >>> p = ccy.currency_pair('eurusd')\n    >>> p\n    ccy_pair: EURUSD\n    >>> p.mkt()  # market convention pair\n    ccy_pair: EURUSD\n    >>> p = ccy.currency_pair('chfusd')\n    >>> p\n    ccy_pair: CHFUSD\n    >>> p.mkt()  # market convention pair\n    ccy_pair: USDCHF\n\n\nSome shortcuts::\n\n    >>> import ccy\n    >>> ccy.cross('aud')\n    'AUDUSD'\n    >>> ccy.crossover('eur')\n    'EUR/USD'\n    >>> ccy.crossover('chf')\n    'USD/CHF'\n\nNote, the Swiss franc cross is represented as 'USD/CHF', while the Aussie Dollar\nand Euro crosses are represented with the USD as denominator.\nThis is the market convention which is handled by the **order** property\nof a currency object.\n\nCountry information\n~~~~~~~~~~~~~~~~~~~~~~~~~~\n\nTo use it::\n\n    >>> import ccy\n    >>> c = ccy.country('us')\n    >>> c\n    'United States'\n    >>> ccy.countryccy('us')\n    'USD'\n\n\nNot all the country codes are standard `ISO 3166-1 alpha-2`_.\nThere is a function for adding extra pseudo-countries::\n\n    import ccy\n    ccy.set_new_country('EU','EUR','Eurozone')\n\nSet a new country with code 'EU', currency 'EUR' named 'Eurozone'.\nThis pseudo country is set in the library already.\n\nCountries\n==============\n\nCountry information is obtained via the pytz_ package which is strict\nrequirement for ``ccy``::\n\n    >>> from ccy import country\n    >>> country('it')\n    'Italy'\n\nIt knows about the 18 eurozone_ countries (European countries which share the\neuro as common currency)::\n\n    >>> from ccy import eurozone\n\neurozone is tuple of country ISO codes::\n\n    >>> import ccy\n    >>> ccy.print_eurozone()\n    Austria\n    Belgium\n    Cyprus\n    Estonia\n    Finland\n    France\n    Germany\n    Greece\n    Ireland\n    Italy\n    Latvia\n    Lithuania\n    Luxembourg\n    Malta\n    Netherlands\n    Portugal\n    Slovakia\n    Slovenia\n    Spain\n\n\nDate and Periods\n===================\n\nThe module is shipped with a ``date`` module for manipulating time periods and\nconverting dates between different formats. The *period* function can be used\nto create ``Period`` instances::\n\n    >>> from ccy import period\n    >>> p = period('1m')\n    >>> p\n    1M\n    >>> p += '2w'\n    >>> p\n    1M2W\n    >>> P += '3m'\n    >>> p\n    4M2W\n\n\nInstallation\n================\nThis library works for Python 2.6 and higher, including Python 3.\nIn addition, it requires:\n\n* pytz_ for Countries information.\n* dateutils_ for date calculations\n\nInstall using ``pip``::\n\n    pip install ccy\n\nor from source::\n\n    python setup.py install\n\n\nRunning tests\n~~~~~~~~~~~~~~~~~~~~~\n\nFrom within the package directory::\n\n    python setup.py test\n\n\n.. _pytz: http://pytz.sourceforge.net/\n.. _`ISO 3166-1 alpha-2`: http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2\n.. _`ISO 4217`: http://en.wikipedia.org/wiki/ISO_4217\n.. _dateutils: https://pypi.python.org/pypi/python-dateutil\n.. _eurozone: http://www.eurozone.europa.eu/euro-area/euro-area-member-states/\n",
    'author': 'Luca Sbardella',
    'author_email': 'luca@quantmind.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)

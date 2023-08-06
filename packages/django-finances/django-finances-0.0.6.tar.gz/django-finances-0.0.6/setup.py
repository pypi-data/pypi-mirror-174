# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_finances',
 'django_finances.migrations',
 'django_finances.payments',
 'django_finances.payments.migrations',
 'django_finances.payments.providers',
 'django_finances.payments.providers.invoice',
 'django_finances.payments.providers.mollie',
 'django_finances.payments.providers.mollie.migrations',
 'django_finances.payments.providers.sepa',
 'django_finances.templatetags',
 'django_finances.transactions',
 'django_finances.transactions.migrations']

package_data = \
{'': ['*'],
 'django_finances': ['data/*', 'locale/nl/LC_MESSAGES/*'],
 'django_finances.payments': ['locale/nl/LC_MESSAGES/*'],
 'django_finances.payments.providers.sepa': ['templates/payments/providers/sepa/*'],
 'django_finances.transactions': ['locale/nl/LC_MESSAGES/*']}

install_requires = \
['django>=4.0,<5.0', 'lxml>=4.9.0,<5.0.0', 'python-dateutil>=2.8.2,<3.0.0']

setup_kwargs = {
    'name': 'django-finances',
    'version': '0.0.6',
    'description': 'Financial transactions and payments for Django.',
    'long_description': '# Django Finances\n\nFinancial transactions and payments for Django.\n\n**NOTE: This library is still under development and mostly undocumented. It is currently not recommended for use in (production) applications.**\n\n## Features\n\nThis library consists of two modules: transactions and payments. The two modules were designed to be used together, but they can also be used separately.\n\n### Transactions\nTransactions are TODO\n\n### Payments\nPayments are TODO\n\n#### Payment providers\n- Invoice\n- [Mollie](https://www.mollie.com)\n- [SEPA Direct Debit](https://www.europeanpaymentscouncil.eu/what-we-do/sepa-direct-debit)\n\n## Documentation\nThe documentation is available [here](docs/index.md).\n\n## Contributing\nSee the [development documentation](docs/development.md). In the future more specific guidelines for contributing will be drafted. \n\n## License\nThis project is available under the [MIT license](LICENSE.md). Note that some dependencies have different licenses.\n',
    'author': 'Daniel Huisman',
    'author_email': 'daniel@huisman.me',
    'maintainer': 'Daniel Huisman',
    'maintainer_email': 'daniel@huisman.me',
    'url': 'https://github.com/DanielHuisman/django-finances',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

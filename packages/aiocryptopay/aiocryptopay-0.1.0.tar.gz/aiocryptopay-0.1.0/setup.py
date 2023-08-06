# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiocryptopay', 'aiocryptopay.exceptions', 'aiocryptopay.models']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.3,<4.0.0',
 'certifi>=2022.9.14,<2023.0.0',
 'pydantic>=1.10.2,<2.0.0']

setup_kwargs = {
    'name': 'aiocryptopay',
    'version': '0.1.0',
    'description': '@cryptobot api asynchronous python wrapper',
    'long_description': "## **[@cryptobot](https://t.me/CryptoBot) asynchronous api wrapper**\n**Docs:** https://help.crypt.bot/crypto-pay-api\n\n - MainNet - [@CryptoBot](http://t.me/CryptoBot)\n - TestNet - [@CryptoTestnetBot](http://t.me/CryptoTestnetBot)\n\n\n**Basic methods**\n``` python\nfrom aiocryptopay import AioCryptoPay, Networks\n\napi = AioCryptoPay(token='1337:JHigdsaASq', network=Networks.MAIN_NET)\n\nprofile = await api.get_me()\ncurrencies = await api.get_currencies()\nbalance = await api.get_balance()\nrates = await api.get_exchange_rates()\n\nprint(profile, currencies, balance, rates, sep='\\n')\n```\n\n**Create and get invoice methods**\n``` python\nfrom aiocryptopay import AioCryptoPay, Networks\n\napi = AioCryptoPay(token='1337:JHigdsaASq', network=Networks.MAIN_NET)\n\ninvoice = await api.create_invoice(asset='TON', amount=1.5)\nprint(invoice.pay_url)\n\ninvoices = await api.get_invoices(invoice_ids=invoice.invoice_id)\nprint(invoices.status)\n```",
    'author': 'layerqa',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/layerqa/aiocryptopay',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

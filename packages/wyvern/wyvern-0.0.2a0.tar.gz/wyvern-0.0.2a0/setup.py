# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wyvern',
 'wyvern.commands',
 'wyvern.components',
 'wyvern.constructors',
 'wyvern.gateway',
 'wyvern.interactions',
 'wyvern.models',
 'wyvern.rest',
 'wyvern.state_handlers']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0', 'attrs>=22.1.0,<23.0.0']

setup_kwargs = {
    'name': 'wyvern',
    'version': '0.0.2a0',
    'description': 'A flexible and easy to use Discord API wrapper for python 🚀.',
    'long_description': '# wyvern\n![](https://img.shields.io/github/license/sarthhh/asuka?style=flat-square)\n![](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)\n![](https://img.shields.io/badge/%20type_checker-mypy-%231674b1?style=flat-square)\n![](https://img.shields.io/github/stars/sarthhh/asuka?style=flat-square)\n![](https://img.shields.io/github/last-commit/sarthhh/asuka?style=flat-square)\n\nA flexible and easy to use Discord API wrapper for python 🚀.\n\n## Why use wyvern? \n* Feature rich API.\n* Full control over the library\'s functionality.\n* Built-in extensions for prefix commands.\n* Interaction commands handling.\n\n## Installation\n```sh\n# from pypi \n$python -m pip install wyvern\n# from source stable branch\n$python -m pip install git+https://github.com/sarthhh/wyvern@main\n# from source development branch \n$pythonn -m pip install git+https://github.com/sarthhh/wyvern\n```\n\n## Example Code:\n* Basic GatewayClient with listener. \n```py\nimport wyvern\n\n# creating a GatewayClient instance and storing it into the client variable.\n# this acts as the interface between your bot and the code.\n\nclient = wyvern.GatewayClient("TOKEN", intents=wyvern.Intents.UNPRIVILEGED | wyvern.Intents.MESSAGE_CONTENT)\n\n# creating an EventListener object and adding it to the client\'s event handler using the\n# @client.listen decorator. You can set the maximum amount of time this listener will get triggered using\n# the `max_trigger kwarg in the listener decorator.`\n\n\n@client.listener(wyvern.Event.MESSAGE_CREATE)\nasync def message_create(message: wyvern.Message) -> None:\n    """This coroutine is triggerd whenever the MESSAGE_CREATE event gets dispatched."""\n    if message.content and message.content.lower() == "!ping":\n        await message.respond("pong!")\n\n\n# runs the bot.\n\nclient.run()\n```\n* GatewayClient with custom event handler.\n```py\nimport wyvern\n\n# subclassing to create a new EventHandler class.\n# events listeners can be added using the @wyvern.listener decorator.\n# the client can be accessed using client attribute inside the listener.\n\n\nclass MyHandler(wyvern.EventHandler):\n    @wyvern.listener(wyvern.Event.MESSAGE_CREATE)\n    async def message_create(self, message: wyvern.Message) -> None:\n        print(f"Message sent by {message.author.username}")\n\n\n# the subclass\' type ( !not instance ) is provided for the event_handler kwarg inside\n# the client class. which uses this custom EventHandler instead of a default one.\n\nclient = wyvern.GatewayClient("TOKEN", event_handler=MyHandler)\n\n# runs the bot.\n\nclient.run()\n```',
    'author': 'sarthhh',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

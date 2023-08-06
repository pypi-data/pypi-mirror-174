# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asyncclick_repl']

package_data = \
{'': ['*']}

install_requires = \
['anyio>=3.2.1,<4.0.0',
 'asyncclick>=8.1.3.4,<9.0.0.0',
 'prompt-toolkit>=3.0.31,<4.0.0']

setup_kwargs = {
    'name': 'asyncclick-repl',
    'version': '0.1.1',
    'description': 'Command class to add REPL support to existing click groups',
    'long_description': '# asyncclick-repl\n\nCommand to make a REPL out of a group by passing `-i` or `--interactive` to the cli.\nInspired by [click-repl](https://github.com/click-contrib/click-repl) but using native\nclick command and shell completion.\n\n```python\nimport asyncio\n\nimport asyncclick as click\n\nfrom asyncclick_repl import AsyncREPL\n\n\n@click.group(cls=AsyncREPL)\nasync def cli():\n    pass\n\n\n@cli.command()\n@click.option("--count", default=1, help="Number of greetings.")\n@click.option("--name", prompt="Your name", help="The person to greet.")\nasync def hello(count, name):\n    """Simple program that greets NAME for a total of COUNT times."""\n    for _ in range(count):\n        await asyncio.sleep(0.1)\n        click.echo(f"Hello, {name}!")\n\n\ncli(_anyio_backend="asyncio")\n```\n\n```shell\nmyclickapp -i\n\n> hello --count 2 --name Foo\nHello, Foo!\nHello, Foo!\n> :q\n```\n\n# Features:\n\n- Tab-completion. Using click\'s shell completion\n- Execute system commands using `!` prefix. Note: `!` should be followed by a space e.g `! ls`\n- `:h` show commands help.\n\n# Prompt configuration\n\nUse `prompt_kwargs` to provide configuration to `python-prompt-toolkit`\'s `Prompt` class\n\n```python\nimport asyncclick as click\nfrom prompt_toolkit.history import FileHistory\n\nfrom asyncclick_repl import AsyncREPL\n\nprompt_kwargs = {\n    "history": FileHistory("./history"),\n}\n\n\n@click.group(cls=AsyncREPL, prompt_kwargs=prompt_kwargs)\nasync def cli():\n    pass\n\n\ncli()\n```\n',
    'author': 'Federico Jaite',
    'author_email': 'fede_654_87@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/fedej/asyncclick-repl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

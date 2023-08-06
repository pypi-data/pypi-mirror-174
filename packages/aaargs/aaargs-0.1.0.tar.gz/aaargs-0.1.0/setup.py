# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aaargs']

package_data = \
{'': ['*']}

install_requires = \
['zninit>=0.1.1,<0.2.0']

setup_kwargs = {
    'name': 'aaargs',
    'version': '0.1.0',
    'description': 'autocompletion and argument parsing',
    'long_description': '[![coveralls](https://coveralls.io/repos/github/zincware/aaargs/badge.svg)](https://coveralls.io/github/zincware/aaargs)\n![PyTest](https://github.com/zincware/aaargs/actions/workflows/pytest.yaml/badge.svg)\n[![PyPI version](https://badge.fury.io/py/aaargs.svg)](https://badge.fury.io/py/aaargs)\n\n# Aaargs ...\n\nI\'m not a huge fan of the [argparse](https://docs.python.org/3/library/argparse.html) library that ships with Python.\nPersonally, I much prefer  [typer](https://typer.tiangolo.com/) or [click](https://click.palletsprojects.com/).\nBut `argparse` is often used so this is my approach in bringing at least autocompletion to the argparse library.\n\nLet us take a look at the official documentation and use their examples:\n\n```python\nimport argparse\n\nparser = argparse.ArgumentParser(\n                    prog = \'ProgramName\',\n                    description = \'What the program does\',\n                    epilog = \'Text at the bottom of help\')\n\nparser.add_argument(\'filename\')           # positional argument\nparser.add_argument(\'-c\', \'--count\')      # option that takes a value\nparser.add_argument(\'-v\', \'--verbose\',\n                    action=\'store_true\')  # on/off flag\n\nargs = parser.parse_args()\nprint(args.filename, args.count, args.verbose)\n```\n\nWhy isn\'t the `argparse.ArgumentParser` a container class, like a dataclass?\n\nSo my approach to *solve* this looks like this:\n\n```python\nfrom aaargs import ArgumentParser, Argument\n\nclass MyParser(ArgumentParser):\n    rog = "ProgramName"\n    description = "What the program does"\n    epilog = "Text at the bottom of help"\n\n    # You can define arguments directly\n    filename = Argument()  # positional argument\n    encoding = Argument(positional=False)  # keyword argument \'--encoding\'\n    \n    # or pass the \'name_or_flags\' argument\n    count = Argument("-c", "--count")\n    verbose = Argument("-v", "--verbose", action="store_true")\n\nparser: argparse.ArgumentParser = MyParser.get_parser()\nargs: MyParser = MyParser.parse_args()\n```\n\nYou can also print the parser just like the original:\n```python\nargs = MyParser.parse_args(\n        ["README.md", "--encoding", "utf-8", "-c", "3"]\n    )\n\nprint(args)\n>>> MyParser(count=\'3\', encoding=\'utf-8\', filename=\'README.md\', verbose=False)\n```\n\nYou can also create a Parser using keyword arguments if you prefer (I don\'t):\n\n```python\nfrom aaargs import ArgumentParser\n\nclass MyParser(\n    ArgumentParser,\n    prog="ProgramName",\n    description="What the program does",\n    epilog="Text at the bottom of help",\n):\n    ...\n```',
    'author': 'zincwarecode',
    'author_email': 'zincwarecode@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

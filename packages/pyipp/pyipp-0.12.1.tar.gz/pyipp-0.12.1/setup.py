# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyipp']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.0.0',
 'awesomeversion>=21.10.1',
 'backoff>=1.9.0',
 'deepmerge>=0.1.0',
 'yarl>=1.6.0']

setup_kwargs = {
    'name': 'pyipp',
    'version': '0.12.1',
    'description': 'Asynchronous Python client for Internet Printing Protocol (IPP)',
    'long_description': '# Python: Internet Printing Protocol (IPP) Client\n\nAsynchronous Python client for Internet Printing Protocol (IPP).\n\n## About\n\nThis package allows you to monitor printers that support the Internet Printing Protocol (IPP) programmatically.\n\n## Installation\n\n```bash\npip install pyipp\n```\n\n## Usage\n\n```python\nimport asyncio\n\nfrom pyipp import IPP, Printer\n\n\nasync def main():\n    """Show example of connecting to your IPP print server."""\n    async with IPP("ipps://EPSON123456.local:631/ipp/print") as ipp:\n        printer: Printer = await ipp.printer()\n        print(printer)\n\n\nif __name__ == "__main__":\n    loop = asyncio.get_event_loop()\n    loop.run_until_complete(main())\n```\n\n## Setting up development environment\n\nThis Python project is fully managed using the [Poetry](https://python-poetry.org) dependency\nmanager. But also relies on the use of NodeJS for certain checks during\ndevelopment.\n\nYou need at least:\n\n- Python 3.9+\n- [Poetry](https://python-poetry.org/docs/#installation)\n- NodeJS 16+ (including NPM)\n\nTo install all packages, including all development requirements:\n\n```bash\nnpm install\npoetry install\n```\n\nAs this repository uses the [pre-commit](https://pre-commit.com/) framework, all changes\nare linted and tested with each commit. You can run all checks and tests\nmanually, using the following command:\n\n```bash\npoetry run pre-commit run --all-files\n```\n\nTo run just the Python tests:\n\n```bash\npoetry run pytest\n```\n',
    'author': 'Chris Talkington',
    'author_email': 'chris@talkingtontech.com',
    'maintainer': 'Chris Talkington',
    'maintainer_email': 'chris@talkingtontech.com',
    'url': 'https://github.com/ctalkington/python-ipp',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

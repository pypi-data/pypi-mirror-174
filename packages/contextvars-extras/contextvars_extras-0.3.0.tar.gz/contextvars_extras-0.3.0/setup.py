# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['contextvars_extras', 'contextvars_extras.integrations']

package_data = \
{'': ['*']}

install_requires = \
['sentinel-value>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'contextvars-extras',
    'version': '0.3.0',
    'description': 'Contextvars made easy (WARNING: unstable alpha version. Things may break).',
    'long_description': "contextvars-extras\n==================\n\n|pypi badge| |build badge| |docs badge|\n\n``contextvars-extras`` is a set of extensions for the Python's `contextvars`_ module.\n\nIn case you are not familiar with the `contextvars`_ module, its `ContextVar`_ objects\nwork like Thread-Local storage, but better: they are both thread-safe and async task-safe,\nand they can be copied (all existing vars copied in O(1) time), and then you can run\na function in the copied and isolated context.\n\n.. _contextvars: https://docs.python.org/3/library/contextvars.html\n.. _ContextVar: https://docs.python.org/3/library/contextvars.html#contextvars.ContextVar\n\nThe `contextvars`_ is a powerful module, but its API seems too low-level.\n\nSo this ``contextvars_extras`` package provides some higher-level additions on top of the\nstandard API, like, for example, organizing `ContextVar`_ objects into registry classes,\nwith nice ``@property``-like access:\n\n.. code:: python\n\n    from contextvars_extras import ContextVarsRegistry\n\n    class CurrentVars(ContextVarsRegistry):\n        locale: str = 'en'\n        timezone: str = 'UTC'\n\n    current = CurrentVars()\n\n    # calls ContextVar.get() under the hood\n    current.timezone  # => 'UTC'\n\n    # calls ContextVar.set() under the hood\n    current.timezone = 'GMT'\n\n    # ContextVar() objects can be reached as class members\n    CurrentVars.timezone.get()  # => 'GMT'\n\nThat makes your code more readable (no more noisy ``.get()`` calls),\nand it is naturally firendly to `typing`_, so static code analysis features\n(like type checkers and auto-completion in your IDE) work nicely.\n\n.. _typing: https://docs.python.org/3/library/typing.html\n\nCheck out the `full documentation <https://contextvars-extras.readthedocs.io>`_\n\nLinks\n-----\n\n- Read the Docs: https://contextvars-extras.readthedocs.io\n- GitHub repository: https://github.com/vdmit11/contextvars-extras\n- Python package: https://pypi.org/project/contextvars-extras/\n\n\n.. |pypi badge| image:: https://img.shields.io/pypi/v/contextvars-extras.svg\n  :target: https://pypi.org/project/contextvars-extras/\n  :alt: Python package version\n\n.. |build badge| image:: https://github.com/vdmit11/contextvars-extras/actions/workflows/build.yml/badge.svg\n  :target: https://github.com/vdmit11/contextvars-extras/actions/workflows/build.yml\n  :alt: Tests Status\n\n.. |docs badge| image:: https://readthedocs.org/projects/contextvars-extras/badge/?version=latest\n  :target: https://contextvars-extras.readthedocs.io/en/latest/?badge=latest\n  :alt: Documentation Status\n\n",
    'author': 'Dmitry Vasilyanov',
    'author_email': 'vdmit11@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/vdmit11/contextvars-extras',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)

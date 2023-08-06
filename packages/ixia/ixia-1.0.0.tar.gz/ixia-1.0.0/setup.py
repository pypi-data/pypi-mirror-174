# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ixia']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ixia',
    'version': '1.0.0',
    'description': "A library connecting secrets' security with random's versatility",
    'long_description': "# Ixia\nIxia is a cryptographically secure RNG library. It mainly merges `secrets`'\nsecurity with `random`'s versatility, but also adds some of its own\nfunctions, such as [`ixia.passphrase()`](https://trag1c.github.io/ixia/sequences.html#ixiapassphrase), [`ixia.shuffled()`](https://trag1c.github.io/ixia/sequences.html#ixiashuffled) or\n[`ixia.universe_rand()`](https://trag1c.github.io/ixia/bytes_and_integers.html#ixiauniverse_rand). All random values are generated using `urandom` (or `BCryptGenRandom` on Windows).\n\n## Installation\nIxia is available on PyPI and can be installed with pip, or any other Python package manager:\n```sh\n$ pip install dahlia\n```\n(Some systems may require you to use `pip3`, `python -m pip`, or `py -m pip` instead.)\n\n## Documentation\nIxia documentation is available at https://trag1c.github.io/ixia/.\n\n## License\nIxia is licensed under the MIT License.\n\n## ⚠️ Important Notes\nWhile supporting Python 3.8+, Ixia is based on the Python 3.10 implementation\nof the `random` module. The following changes have been made to the module\nsince Python 3.8:\n- `getrandbits` accepts 0 for `k`\n- `choices` raises a `ValueError` if all weights are zero\n- `sample` has a new `counts` parameter\n\nAdditionally, Ixia executes 3.9 and 3.10 deprecations, thus:\n- `ixia.rand_range` doesn't convert non-integer types to equivalent integers\n- `ixia.sample` doesn't support `set` as a sequence type\n- `ixia.shuffle` doesn't support the `random` parameter\n",
    'author': 'trag1c',
    'author_email': 'trag1cdev@yahoo.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/trag1c/ixia',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['amr_logic_converter']

package_data = \
{'': ['*']}

install_requires = \
['Penman>=1.2.2,<2.0.0', 'typing-extensions>=3.7.4']

setup_kwargs = {
    'name': 'amr-logic-converter',
    'version': '0.4.0',
    'description': 'Convert Abstract Meaning Representation (AMR) into first-order logic',
    'long_description': '# AMR Logic Converter\n\n[![ci](https://img.shields.io/github/workflow/status/chanind/amr-logic-converter/CI/main)](https://github.com/chanind/amr-logic-converter)\n[![Codecov](https://img.shields.io/codecov/c/github/chanind/amr-logic-converter/main)](https://codecov.io/gh/chanind/amr-logic-converter)\n[![PyPI](https://img.shields.io/pypi/v/amr-logic-converter?color=blue)](https://pypi.org/project/amr-logic-converter/)\n\nConvert Abstract Meaning Representation (AMR) to first-order logic statements.\n\nThis library is based on the ideas in the paper ["Expressive Power of Abstract Meaning Representations", J. Bos, Computational Linguistics 42(3), 2016](http://www.mitpressjournals.org/doi/pdf/10.1162/COLI_a_00257). Thank you to [@jobos](https://github.com/jobos) for the paper!\n\n## Installation\n\n```\npip install amr-logic-converter\n```\n\n## Usage\n\nThis library parses an AMR tree into first-order logic statements. An example of this is shown below:\n\n```python\nfrom amr_logic_converter import AmrLogicConverter\n\nconverter = AmrLogicConverter()\n\nAMR = """\n(x / boy\n    :ARG0-of (e / giggle-01\n        :polarity -))\n"""\n\nlogic = converter.convert(AMR)\nprint(logic)\n# boy(x) ^ ¬(:ARG0(e, x) ^ giggle-01(e))\n```\n\n### Programmatic logic manipulation\n\nThe output from the `convert` method can be displayed as a string, but it can also be manipulated in Python. For instance, in the example above, we could also write:\n\n```python\nconverter = AmrLogicConverter()\n\nAMR = """\n(x / boy\n    :ARG0-of (e / giggle-01\n        :polarity -))\n"""\n\nexpr = converter.convert(AMR)\ntype(expr) # <class \'amr_logic_converter.types.And\'>\nlogic.args[0] # Predicate(value=\'boy\', args=(Const(name=\'x\', type=\'instance\'),), alignment=None)\n```\n\n### Working with alignment markers\n\nThis library will parse alignment markers from AMR using the [penman library](https://penman.readthedocs.io/en/latest/), and will include [Alignment](https://penman.readthedocs.io/en/latest/api/penman.surface.html#penman.surface.Alignment) objects from penman in `Predicate` and `Const` objects when available. For example, we can access alignment markers like below:\n\n```python\nconverter = AmrLogicConverter()\n\nAMR = """\n(x / boy~1\n    :ARG0-of (e / giggle-01~3\n        :polarity -))\n"""\n\nexpr = converter.convert(AMR)\nexpr.args[0].alignment # Alignment((1,))\nexpr.args[1].body.args[1].alignment # Alignment((3,))\n```\n\n### Existentially Quantifying all Instances\n\nIn ["Expressive Power of Abstract Meaning Representations"](http://www.mitpressjournals.org/doi/pdf/10.1162/COLI_a_00257), all instances are wrapped by an existence quantifier. By default `AmrLogicConverter` does not include these as it\'s likely not useful, but if you\'d like to include them as in the paper you can pass the option `existentially_quantify_instances=True` when constructing the `AmrLogicConverter` as below:\n\n```python\nconverter = AmrLogicConverter(existentially_quantify_instances=True)\n\nAMR = """\n(x / boy\n    :ARG0-of (e / giggle-01\n        :polarity -))\n"""\n\nlogic = converter.convert(AMR)\nprint(logic)\n# ∃x(boy(x) ^ ¬∃e(:ARG0(e, x) ^ giggle-01(e)))\n```\n\n### Using Variables for Instances\n\nIf you want to use variables for each AMR instance instead of constants, you can pass the option `use_variables_for_instances=True` when creating the AmrLogicConverter instance. When `existentially_quantify_instances` is set, variable will always be used for instances regardless of this setting.\n\n## Contributing\n\nContributions are welcome! Please leave an issue in the Github repo if you find any bugs, and open a pull request with and fixes or improvements that you\'d like to contribute. Ideally please include new test cases to verify any changes or bugfixes if appropriate.\n\nThis project uses [poetry](https://python-poetry.org/) for dependency management and packaging, [black](https://black.readthedocs.io/en/stable/) for code formatting, [flake8](https://flake8.pycqa.org/en/latest/) for linting, and [mypy](https://mypy.readthedocs.io/en/stable/) for type checking.\n\n## License\n\nThis project is licenced under a MIT license.\n',
    'author': 'David Chanin',
    'author_email': 'chanindav@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

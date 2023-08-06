# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['e_lims']

package_data = \
{'': ['*']}

install_requires = \
['bump2version>=1.0.1,<2.0.0', 'typing_extensions>=4.4.0,<5.0.0']

extras_require = \
{'doc': ['Sphinx>=5.3.0,<6.0.0',
         'sphinx-rtd-theme>=1.0.0,<2.0.0',
         'sphinx-autodoc-typehints>=1.19.4,<2.0.0',
         'sphinxcontrib-mermaid>=0.7.1,<0.8.0'],
 'tests': ['pytest>=7.1.3,<8.0.0',
           'pytest-cov>=4.0.0,<5.0.0',
           'pytest-cookies>=0.6.1,<0.7.0']}

setup_kwargs = {
    'name': 'e-lims',
    'version': '0.0.4',
    'description': 'E-lims Cookiecutter Template.',
    'long_description': '======\ne-lims\n======\n|pypi| |license| |docs| |coverage| |Security Rating| |Maintainability|\n\nE-lims Cookiecutter Template.\n\n* Free software: MIT license\n\nFeatures\n--------\n\n* Package template: Cookiecutter_ \n* Packaging and dependency management: Poetry_\n* Formatter: Black_ and Flake8_\n* Type checker: Mypy_\n* Tests framework: Pytest_\n* Automate and standardize testing: Tox_\n* Documentation: Sphinx_\n\n.. |pypi| image:: https://img.shields.io/pypi/v/e-lims\n    :alt: Tag\n    :target: https://pypi.org/project/e-lims/\n  \n.. |license| image:: https://img.shields.io/pypi/l/e-lims\n    :alt: License\n    :target: https://github.com/FabienMeyer/e-lims/blob/main/LICENSE\n\n.. |docs| image:: https://readthedocs.org/projects/e-lims/badge/?version=latest\n    :alt: Documentation Status\n    :target: https://fabienmeyer.github.io/e-lims/\n\n.. |coverage| image:: https://codecov.io/gh/FabienMeyer/e-lims/branch/main/graph/badge.svg?token=H2L1PG5S5A \n    :alt: Test coverage\n    :target: https://codecov.io/gh/FabienMeyer/e-lims\n\n.. |Security Rating| image:: https://sonarcloud.io/api/project_badges/measure?project=FabienMeyer_e-lims&metric=security_rating\n    :alt: Security Rating\n    :target: https://sonarcloud.io/project/overview?id=FabienMeyer_e-lims\n\n.. |Maintainability| image:: https://sonarcloud.io/api/project_badges/measure?project=FabienMeyer_e-lims&metric=sqale_rating\n    :alt: Maintainability\n    :target: https://sonarcloud.io/project/overview?id=FabienMeyer_e-lims\n\n\n.. _Cookiecutter: https://github.com/cookiecutter/cookiecutter\n.. _Poetry: https://python-poetry.org/\n.. _Black: https://black.readthedocs.io/en/stable/\n.. _Flake8: https://flake8.pycqa.org/en/latest/\n.. _Mypy: http://mypy-lang.org/\n.. _Pytest: https://docs.pytest.org/en/stable/\n.. _Tox: http://testrun.org/tox/\n.. _Sphinx: http://sphinx-doc.org/\n',
    'author': 'Fabien Meyer',
    'author_email': 'fabien-meyer@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

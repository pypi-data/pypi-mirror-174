# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pecc']

package_data = \
{'': ['*'], 'pecc': ['data/*']}

install_requires = \
['openpyxl>=3.0.10,<4.0.0', 'pandas>=1.5.1,<2.0.0']

setup_kwargs = {
    'name': 'pecc',
    'version': '0.2.4',
    'description': 'Python Epitopic Charge Calculator',
    'long_description': '[![DOI](https://zenodo.org/badge/555576588.svg)](https://zenodo.org/badge/latestdoi/555576588)\n[![Downloads](https://pepy.tech/badge/pecc)](https://pepy.tech/project/pecc)\n# PECC (Python Epitopic Charge Calculator)\n\n### Overview\nPECC is a Python package designed to calculate efficiently the HLA Epitopic Charge (based on the\n[EpRegistry database](https://www.epregistry.com.br/)) between donors and recipients by loading in a pandas.DataFrame\nin `epitope_comparison.compute_epitopic_charge`.  See minimal reproducible example for more details.\n\n\n### Getting started\n#### Install from PyPI (recommended)\nTo use `pecc`, run `pip install pecc` in your terminal.\n\n\n#### Usage\nHere is a minimal example with the file [Template.xlsx](https://github.com/MICS-Lab/pecc/raw/main/Template.xlsx) (click to download):\n```py\nimport pandas as pd\n\nfrom pecc import epitope_comparison, epitope_comparison_aux, output_type\n\n\nif __name__ == "__main__":\n    input_path: str = "Template.xlsx"\n\n    output_path: str = "MyOutput"\n    input_df: pd.DataFrame = pd.read_excel(\n        input_path, sheet_name="My Sheet", index_col="Index"\n    )\n\n    donordf: pd.DataFrame\n    recipientdf: pd.DataFrame\n    donordf, recipientdf = epitope_comparison_aux.split_dataframe(input_df)\n\n    epitope_comparison.compute_epitopic_charge(\n        donordf,\n        recipientdf,\n        output_path,\n        output_type.OutputType.DETAILS_AND_COUNT\n    )\n```\n\n#### Exit codes:\n```\nNone yet.\n```\n\n\n#### Unit tests\nTested on `Python 3.10.2` & `Python 3.11.0`.\n```\nplatform win32 -- Python 3.10.2, pytest-7.2.0, pluggy-1.0.0\nrootdir: C:\\Users\\lhott\\Documents\\Formation scolaire\\These\\Travail\\pecc\nplugins: mypy-0.10.0\ncollected 19 items                                                                                                                                     \n\nunit_tests_mypy.py ..                                                               [ 10%]\nunit_tests_simple.py .                                                              [ 15%] \npecc\\__init__.py .                                                                  [ 21%] \npecc\\_unexpected_alleles.py .                                                       [ 26%] \npecc\\epitope_comparison.py .                                                        [ 31%] \npecc\\epitope_comparison_aux.py .                                                    [ 36%] \npecc\\output_type.py .                                                               [ 42%] \ntests\\__init__.py .                                                                 [ 47%] \ntests\\base_loading_for_tests.py .                                                   [ 52%] \ntests\\test_epitope_mismatches.py ......                                             [ 78%]\ntests\\test_pecc.py ..                                                               [ 89%] \ntests\\test_unexpected_alleles.py ..                                                 [100%]\n```\n```\nplatform win32 -- Python 3.11.0, pytest-7.2.0, pluggy-1.0.0\nplugins: mypy-0.10.0\ncollected 19 items\n\nunit_tests_mypy.py ..                                                               [ 10%]\nunit_tests_simple.py .                                                              [ 15%]\npecc\\__init__.py .                                                                  [ 21%]\npecc\\_unexpected_alleles.py .                                                       [ 26%]\npecc\\epitope_comparison.py .                                                        [ 31%]\npecc\\epitope_comparison_aux.py .                                                    [ 36%]\npecc\\output_type.py .                                                               [ 42%]\ntests\\__init__.py .                                                                 [ 47%]\ntests\\base_loading_for_tests.py .                                                   [ 52%]\ntests\\test_epitope_mismatches.py ......                                             [ 78%]\ntests\\test_pecc.py ..                                                               [ 89%]\ntests\\test_unexpected_alleles.py ..                                                 [100%]\n```\n\n\n\n### About the source code\n- Follows [PEP8](https://peps.python.org/pep-0008/) Style Guidelines.\n- All variables are correctly type-hinted, reviewed with [static type checker](https://mypy.readthedocs.io/en/stable/)\n`mypy`.\n\n\n\n### Useful links:\n- [Corresponding GitHub repository](https://github.com/MICS-Lab/pecc)\n- [Corresponding PyPI page](https://pypi.org/project/pecc)\n\n\n\n### Citation\nIf you use this software, please cite it as below.\n\n- APA:\n```\nLhotte, R., Usureau, C., & Taupin, J. (2022). Python Epitope Charge Calculator (Version 0.2.4) [Computer software].\nhttps://doi.org/10.5281/zenodo.7254809\n```\n\n- BibTeX:\n```\n@software{Lhotte_Python_Epitope_Charge_2022,\n    author = {Lhotte, Romain and Usureau, Cédric and Taupin, Jean-Luc},\n    doi = {doi.org/10.5281/zenodo.7254809},\n    month = {10},\n    title = {{Python Epitope Charge Calculator}},\n    version = {0.2.4},\n    year = {2022}\n}\n```\n',
    'author': 'JasonMendoza2008',
    'author_email': 'lhotteromain@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

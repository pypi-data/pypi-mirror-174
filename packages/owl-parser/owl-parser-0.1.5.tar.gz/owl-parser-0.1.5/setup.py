# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['owl_parser',
 'owl_parser.multiquery',
 'owl_parser.multiquery.bp',
 'owl_parser.multiquery.dmo',
 'owl_parser.multiquery.dmo.span',
 'owl_parser.multiquery.svc',
 'owl_parser.multiquery.tests',
 'owl_parser.mutato',
 'owl_parser.mutato.bp',
 'owl_parser.mutato.dmo',
 'owl_parser.mutato.dmo.core',
 'owl_parser.mutato.dmo.exact',
 'owl_parser.mutato.dmo.hierarchy',
 'owl_parser.mutato.dmo.spans',
 'owl_parser.mutato.dto',
 'owl_parser.mutato.svc',
 'owl_parser.singlequery',
 'owl_parser.singlequery.bp',
 'owl_parser.singlequery.dmo',
 'owl_parser.singlequery.dto',
 'owl_parser.singlequery.svc',
 'owl_parser.singlequery.tests']

package_data = \
{'': ['*']}

install_requires = \
['baseblock', 'owl-builder', 'regression-framework']

setup_kwargs = {
    'name': 'owl-parser',
    'version': '0.1.5',
    'description': 'Parse Input Text using One-or-More Ontology (OWL) files',
    'long_description': '# Ontology Parser (owl-parser)\nUse an Ontology model to parse unstructured text\n\n## Under the hood\nThis is the root level method.\n\nThe input parameters and return values have well-described data types.\n```python\ndef owl_parser(tokens: list,\n               ontology_name: str,\n               absolute_path: str) -> list:\n\n    Enforcer.is_list_of_dicts(tokens)\n    Enforcer.is_str(ontology_name)\n    FileIO.exists_or_error(absolute_path)\n\n    from owl_parser.multiquery.bp import FindOntologyData\n    from owl_parser.mutato.bp import MutatoAPI\n\n    finder = FindOntologyData(ontologies=[ontology_name],\n                              absolute_path=absolute_path)\n\n    results = MutatoAPI(finder).swap(tokens)\n    Enforcer.is_list_of_dicts(results)\n\n    return results\n```\n\n## Import\n```python\nfrom owl_parser import owl_parser\n```\n\n## Usage\n```python\nresults = owl_parser(\n    tokens,\n    ontology_name="<ontology-name>",\n    absolute_path="<absolute-path>")\n',
    'author': 'Craig Trim',
    'author_email': 'craigtrim@gmail.com',
    'maintainer': 'Craig Trim',
    'maintainer_email': 'craigtrim@gmail.com',
    'url': 'https://github.com/craigtrim/owl-parser',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '==3.8.5',
}


setup(**setup_kwargs)

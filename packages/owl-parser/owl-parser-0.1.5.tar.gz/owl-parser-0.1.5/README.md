# Ontology Parser (owl-parser)
Use an Ontology model to parse unstructured text

## Under the hood
This is the root level method.

The input parameters and return values have well-described data types.
```python
def owl_parser(tokens: list,
               ontology_name: str,
               absolute_path: str) -> list:

    Enforcer.is_list_of_dicts(tokens)
    Enforcer.is_str(ontology_name)
    FileIO.exists_or_error(absolute_path)

    from owl_parser.multiquery.bp import FindOntologyData
    from owl_parser.mutato.bp import MutatoAPI

    finder = FindOntologyData(ontologies=[ontology_name],
                              absolute_path=absolute_path)

    results = MutatoAPI(finder).swap(tokens)
    Enforcer.is_list_of_dicts(results)

    return results
```

## Import
```python
from owl_parser import owl_parser
```

## Usage
```python
results = owl_parser(
    tokens,
    ontology_name="<ontology-name>",
    absolute_path="<absolute-path>")

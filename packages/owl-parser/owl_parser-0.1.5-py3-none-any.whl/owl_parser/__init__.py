from baseblock import Enforcer, FileIO

from .multiquery import *
from .mutato import *
from .singlequery import *


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


def find_ontology_data(ontology_name: str, file_path: str) -> FindOntologyData:
    """ Initialize a Finder Object
    Args:
        ontology_name (str): the name of the Ontology
        file_path (str): the absolute path to this Ontology on the local filesystem
    Returns:
        FindOntologyData: an instantiated finder object
    """
    return FindOntologyData(ontologies=[ontology_name], absolute_path=file_path)

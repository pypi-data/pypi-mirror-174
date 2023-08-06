from baseblock import FileIO
from rdflib import Graph

from owl_parser.singlequery.svc import LoadOntologyModel

absolute_path = FileIO.join_cwd('resources/testing')


def test_service():

    svc = LoadOntologyModel(
        ontology_name='askowltest',
        absolute_path=absolute_path)

    assert svc

    g = svc.process()
    assert g
    assert type(g) == Graph


def main():
    test_service()


if __name__ == '__main__':
    main()

from baseblock import FileIO
from rdflib import Graph

from owl_parser.singlequery.dmo import OwlGraphConnector


def manual_test_component_1():
    absolute_path = FileIO.join_cwd('resources/testing')

    dmo = OwlGraphConnector(prefix='askowltest',
                            namespace='http://graffl.ai/askowltest#',
                            ontology_name='askowltest.owl',
                            absolute_path=absolute_path)
    assert dmo

    g = dmo.graph()
    assert g
    assert type(g) == Graph


def manual_test_component_2():
    absolute_path = FileIO.join(FileIO.local_directory_by_name('BastAI'),
                                'owl/ontologica/0.1.0')

    dmo = OwlGraphConnector(prefix='ontologica',
                            namespace='http://graffl.ai/graffl#',
                            ontology_name='ontologica.owl',
                            absolute_path=absolute_path)
    assert dmo

    g = dmo.graph()
    assert g
    assert type(g) == Graph


def main():
    manual_test_component_1()
    manual_test_component_2()


if __name__ == '__main__':
    main()

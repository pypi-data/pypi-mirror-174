from baseblock import FileIO

from owl_parser.multiquery.bp import FindOntologyData

absolute_path = FileIO.join_cwd('resources/testing')


class TestFindOntologyData(object):

    def __init__(self,
                 ontology_name: str):
        self.bp = FindOntologyData(
            ontologies=[ontology_name],
            absolute_path=absolute_path)
        assert self.bp

    def implies_by_entity(self) -> list:

        # demonstrate casing doesn't matter
        assert self.bp.implies_by_entity('advisor') == ['thought_leader']
        assert self.bp.implies_by_entity('Advisor') == ['thought_leader']

        # actual path is [ senior_advisor rdfs:subClassOf advisor . advisor implies thought_leader ]
        assert self.bp.transitive('senior advisor', self.bp.implies_by_entity) == [
            'thought_leader']
        assert self.bp.transitive('trusted advisor', self.bp.implies_by_entity) == [
            'thought_leader']


def runner(ontology_name: str) -> None:
    finder = TestFindOntologyData(ontology_name)

    finder.implies_by_entity()


def test_runner():
    runner('skills')


def main():
    runner('skills')


if __name__ == '__main__':
    main()

from pprint import pprint

from baseblock import Enforcer, FileIO

from owl_parser.multiquery.bp import FindOntologyData

absolute_path = FileIO.join_cwd('resources/testing')


class TestFindOntologyData(object):

    def __init__(self,
                 ontology_name: str):
        self.bp = FindOntologyData(
            ontologies=[ontology_name],
            absolute_path=absolute_path)
        assert self.bp

    def by_predicate(self,
                     predicate_name: str) -> dict:
        return self.bp.by_predicate(
            predicate_name=predicate_name,
            to_lowercase=False)

    def by_predicate_rev(self,
                         predicate_name: str) -> dict:
        return self.bp.by_predicate_rev(
            predicate_name=predicate_name,
            to_lowercase=False)


def runner(ontology_name: str) -> None:
    finder = TestFindOntologyData(ontology_name)

    Enforcer.is_dict(finder.by_predicate('owl:backwardCompatibleWith'))
    pprint(finder.by_predicate_rev('owl:backwardCompatibleWith'))


def test_runner():
    runner('skills')


def main():
    runner('skills')


if __name__ == '__main__':
    main()

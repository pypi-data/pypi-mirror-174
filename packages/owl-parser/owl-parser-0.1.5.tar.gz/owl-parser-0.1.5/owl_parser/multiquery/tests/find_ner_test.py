import os

from baseblock import FileIO, Stopwatch

from owl_parser.multiquery.bp import FindOntologyData

absolute_path = FileIO.join_cwd('resources/testing')


class TestFindOntologyData(object):

    def __init__(self,
                 ontology_name: str):
        self.bp = FindOntologyData(
            ontologies=[ontology_name],
            absolute_path=absolute_path)
        assert self.bp

    def find_ner(self):

        sw = Stopwatch()
        self.bp.find_ner('staff')
        self.bp.find_ner('staff')
        self.bp.find_ner('staff')
        self.bp.find_ner('staffing level')
        result = self.bp.find_ner('staff')
        print(str(sw))

        assert result == 'AGENT'


def runner(ontology_name: str) -> None:
    bp = TestFindOntologyData(ontology_name)
    bp.find_ner()


def test_runner():
    runner('unitest')


def main():
    runner('unitest')


if __name__ == '__main__':
    main()

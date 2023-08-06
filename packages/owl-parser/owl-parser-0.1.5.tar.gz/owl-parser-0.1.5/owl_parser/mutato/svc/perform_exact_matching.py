#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Perform Exact Matching """


from baseblock import BaseObject, Enforcer, Stopwatch

from owl_parser.multiquery.bp import FindOntologyData
from owl_parser.mutato.dmo import ExactMatchFinder, ExactMatchSwapper


class PerformExactMatching(BaseObject):
    """ Perform Exact Matching """

    def __init__(self,
                 find_ontology_data: FindOntologyData):
        """ Change Log

        Created:
            20-Oct-2021
            craigtrim@gmail.com
            *   refactored out of 'mutato-api'
                GRAFFL-CORE-0077
        Updated:
            26-May-2022
            craigtrim@gmail.com
            *   treat 'ontologies' param as a list
                https://github.com/grafflr/deepnlu/issues/7
        Updated:
            27-May-2022
            craigtrim@gmail.com
            *   remove all params in place of 'find-ontology-data'
                https://github.com/grafflr/deepnlu/issues/13

        Args:
            find_ontology_data (FindOntologyData): an instantiation of this object
        """
        BaseObject.__init__(self, __name__)
        self._d_lookup = find_ontology_data.lookup()
        self._exact_match_swapper = ExactMatchSwapper(
            find_ontology_data).process

    def _process(self,
                 tokens: list) -> list:

        gram_size = 5
        while gram_size > 0:

            exact_match_finder = ExactMatchFinder(
                gram_size=gram_size,
                d_lookup=self._d_lookup).process

            results = exact_match_finder(tokens)

            if not results:
                gram_size -= 1
                continue

            d_swap = self._exact_match_swapper(results)

            ids = [x['id'] for x in d_swap['swaps']['tokens']]

            merged = []
            for token in tokens:
                if token['id'] not in ids:
                    merged.append(token)
                elif token['id'] == ids[0]:
                    merged.append(d_swap)

            tokens = self._process(merged)

        return tokens

    def process(self,
                tokens: list) -> list:

        if self.isEnabledForDebug:
            Enforcer.is_list(tokens)

        sw = Stopwatch()

        swaps = self._process(tokens)

        if self.isEnabledForInfo:
            self.logger.info('\n'.join([
                'Exact Swapping Completed',
                f'\tTotal Time: {str(sw)}']))

        return swaps

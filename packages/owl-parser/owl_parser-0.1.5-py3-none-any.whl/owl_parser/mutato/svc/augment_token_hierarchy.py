#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Augment Tokens with Descendant and Ancestory Hierarchy for Inference Purposes """


from baseblock import BaseObject, Enforcer, Stopwatch

from owl_parser.multiquery.bp import FindOntologyData


class AugmentTokenHierarchy(BaseObject):
    """ Augment Tokens with Descendant and Ancestory Hierarchy for Inference Purposes """

    def __init__(self,
                 find_ontology_data: FindOntologyData):
        """ Change Log

        Created:
            14-Feb-2022
            craigtrim@gmail.com
            *   https://github.com/grafflr/graffl-core/issues/188
        Updated:
            26-May-2022
            craigtrim@gmail.com
            *   remove 'ontology_name' as a param in pursuit of
                https://github.com/grafflr/deepnlu/issues/7
        Updated:
            27-May-2022
            craigtrim@gmail.com
            *   remove 'ontologies' and integrate 'find-ontology-data'
                https://github.com/grafflr/deepnlu/issues/13

        Args:
            find_ontology_data (FindOntologyData): an instantiation of this object
        """
        BaseObject.__init__(self, __name__)
        self._find_ancestors = find_ontology_data.ancestors
        self._find_descendants = find_ontology_data.descendants

    def _process(self,
                 tokens: list) -> list:
        for token in tokens:
            token['ancestors'] = self._find_ancestors(token['normal'])
            token['descendants'] = self._find_descendants(
                token['normal'])

        return tokens

    def process(self,
                tokens: list) -> list:

        if self.isEnabledForDebug:
            Enforcer.is_list(tokens)

        sw = Stopwatch()

        tokens = self._process(tokens)

        if self.isEnabledForInfo:
            self.logger.info('\n'.join([
                'Hierarchy Augmentation Completed',
                f'\tTotal Time: {str(sw)}']))

        return tokens

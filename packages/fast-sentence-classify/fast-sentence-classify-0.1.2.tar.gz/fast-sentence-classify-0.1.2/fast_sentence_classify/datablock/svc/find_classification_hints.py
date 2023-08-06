# -*- coding: utf-8 -*-

""" Find Classification Hints """


from typing import Dict, Optional

from baseblock import BaseObject


class FindClassificationHints(BaseObject):
    """ Find Classification Hints """

    def __init__(self) -> None:
        """ Change Log

        Created:
            26-Oct-2022
            craigtrim@gmail.com
        """
        BaseObject.__init__(self, __name__)

    def find(self,
             classification: str) -> Optional[Dict[str, int]]:

        classification = classification.lower().strip()

        if classification == 'where_location':
            from fast_sentence_classify.datablock.dto import d_where_location
            return d_where_location

        return None

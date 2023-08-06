# -*- coding: utf-8 -*-

""" Look for Question Type Evidence in Input Text """


from collections import Counter
from pprint import pprint
from typing import Counter as TypedCounter
from typing import Dict, Optional

from baseblock import BaseObject, TextMatcher

from fast_sentence_classify.datablock.dto import d_hints


class FindClassificationEvidence(BaseObject):
    """ Look for Question Type Evidence in Input Text """

    def __init__(self) -> None:
        """ Change Log

        Created:
            26-Oct-2022
            craigtrim@gmail.com
        """
        BaseObject.__init__(self, __name__)

    def process(self,
                input_text: str) -> Optional[str]:

        input_lower = input_text.lower().strip()
        classifications: TypedCounter[str] = Counter()

        for hint in d_hints:

            if TextMatcher.exists(
                    value=hint,
                    input_text=input_lower,
                    case_sensitive=False):

                for classification in d_hints[hint]:
                    classifications.update({classification: 1})

        if not classifications or not len(classifications):
            return None

        d_results = dict(classifications)

        d_rev: Dict[int, str] = {d_results[k]: k for k in d_results}
        if not d_rev or not len(d_rev):
            return None

        high_score = max(list(d_rev.keys()))
        return d_rev[high_score]

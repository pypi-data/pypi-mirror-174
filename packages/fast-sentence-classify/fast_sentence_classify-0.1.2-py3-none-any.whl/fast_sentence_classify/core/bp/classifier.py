# -*- coding: utf-8 -*-

""" Orchestrate Input Classification """


from typing import Any, Dict

from baseblock import Stopwatch
from baseblock import BaseObject
from baseblock import ServiceEventGenerator

from fast_sentence_classify.core.svc import FindClassificationEvidence


class Classifier(BaseObject):
    """ Orchestrate Input Classification """

    def __init__(self) -> None:
        """ Change Log

        Created:
            23-Oct-2022
            craigtrim@gmail.com
        """
        BaseObject.__init__(self, __name__)
        self._service_event = ServiceEventGenerator().process
        self._find_evidence = FindClassificationEvidence().process

    def run(self,
            input_text: str) -> Dict[Any, Any]:
        """ Entry Point

        Args:
            input_text (str): An input string of any length or type

        Raises:
            ValueError: input must be a string

        Returns:

        """
        sw = Stopwatch()

        if not input_text:
            return self._service_event(
                service_name='classify',
                event_name='fast-sentence-classify',
                stopwatch=sw,
                data={
                    'input_text': None,
                    'output_text': None,
                })

        classification = self._find_evidence(input_text)

        return self._service_event(
            service_name='classify',
            event_name='fast-sentence-classify',
            stopwatch=sw,
            data={
                'input_text': input_text,
                'output_text': classification,
            })

from typing import Optional

from baseblock import BaseObject

class FindClassificationEvidence(BaseObject):
    def __init__(self) -> None: ...
    def process(self, input_text: str) -> Optional[str]: ...

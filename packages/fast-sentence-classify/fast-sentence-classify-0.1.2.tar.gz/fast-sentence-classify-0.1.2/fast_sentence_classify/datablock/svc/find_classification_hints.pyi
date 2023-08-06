from typing import Dict, Optional

from baseblock import BaseObject

class FindClassificationHints(BaseObject):
    def __init__(self) -> None: ...
    def find(self, classification: str) -> Optional[Dict[str, int]]: ...

from enum import Enum
from typing import List


class ExtendedStrEnum(str, Enum):
    """Adds list method which will list all values associated with children instances."""

    @classmethod
    def list(cls) -> List[str]:
        return list(map(lambda c: c.value, cls))

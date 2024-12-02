from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class ApiFilter:
    endpoint: str
    params: Dict[str, str]

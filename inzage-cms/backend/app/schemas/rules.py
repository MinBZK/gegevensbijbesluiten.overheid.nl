from enum import Enum

from pydantic import BaseModel


class Importance(Enum):
    INFO = "Info"
    WARNING = "Waarschuwing"
    ERROR = "Fout"
    UNKNOWN = "Onbekend"


class ValidateStructureResult(BaseModel):
    ruleId: int
    name: str
    explanation: str
    importance: Importance
    result: bool
    content: list | None  # Replace with real typing

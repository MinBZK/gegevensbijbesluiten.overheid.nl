from __future__ import annotations

from pydantic import BaseModel


class TableModelColumns(BaseModel):
    COLUMN_NAME: str
    DATA_TYPE: str
    CHARACTER_MAXIMUM_LENGTH: int | None
    COLUMN_TYPE: str
    COLUMN_KEY: str
    IS_NULLABLE: bool


class ForeignKey(BaseModel):
    foreign_key: str
    direction: str
    foreign_resource: str
    foreign_table: TableModel


class TableModel(BaseModel):
    resource: str
    primary_key: str | None
    description_key: str
    fields: dict
    foreign_key_mapping: dict
    foreign_keys: list[ForeignKey]


ForeignKey.model_rebuild()

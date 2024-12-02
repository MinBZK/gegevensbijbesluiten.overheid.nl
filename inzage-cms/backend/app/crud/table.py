import functools
import logging
import os
from typing import Union

from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import Session

import app.config as config
from app.config.resource import TableResource
from app.database.database import Base

# Setup logger
logger = logging.getLogger(__name__)


class TableMeta:
    __slots__ = ["_table_name", "_table_catalog", "_db", "_recursion_level", "_table_mapping", "_resource"]

    def __init__(
        self,
        table_name: str,
        db: Session,
        resource: str,
        recursion_level: int = 0,
    ) -> None:
        self._table_name = table_name
        self._table_catalog = os.getenv("POSTGRES_DB", "inzage-data")
        self._db = db
        self._recursion_level = recursion_level
        self._table_mapping = config.resource.MAPPING_TABLE_TO_RESOURCE[table_name]
        self._resource = resource

    @property
    def __table_class(self):
        """Return class reference mapped to table.

        :return: Class reference or None.
        """

        models = [mapper.class_ for mapper in Base.registry.mappers if mapper.class_.__tablename__ == self._table_name]
        if len(models) == 0:
            return None
        elif len(models) > 1:
            raise ValueError(f"More than 1 model found for given table with name = {self._table_name}.")
        else:
            return models[0]

    def __execute_query(self, query, params: dict) -> list[dict]:
        engine = self._db.get_bind()
        with engine.begin() as conn:
            result = conn.execute(query, params)
            return [dict(zip(row._fields, row)) for row in result]

    @property
    def __sql_columns(self):
        return self.__execute_query(
            query=text(
                """
                SELECT IS_NULLABLE, COLUMN_NAME, DATA_TYPE, case when DATA_TYPE in ('integer') then '11' else CHARACTER_MAXIMUM_LENGTH
                end as CHARACTER_MAXIMUM_LENGTH, TABLE_CATALOG, TABLE_SCHEMA, TABLE_NAME
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_CATALOG = :table_catalog AND TABLE_SCHEMA = 'public' AND TABLE_NAME = :table_name
                """
            ),
            params={
                "table_catalog": self._table_catalog,
                "table_name": self._table_name,
            },
        )

    @property
    def primary_key(self) -> Union[str, None]:
        return self._table_mapping.primary_key

    @property
    def foreign_key_mapping(self) -> dict:
        return self._table_mapping.foreign_key_mapping

    @property
    def __relationships(self) -> list:
        MAX_RECURSION_LEVEL = 1
        if self._recursion_level < MAX_RECURSION_LEVEL:
            i = inspect(self.__table_class)
            return i.relationships
        else:
            return []

    @property
    def description_key(self) -> str:
        description_key = self._table_mapping.description_key
        if description_key is None:
            raise HTTPException(
                status_code=500,
                detail=f"No description key defined for table {self._table_name}",
            )
        return description_key

    @property
    def resource(self) -> str:
        resource = self._table_mapping.resource
        if resource is None:
            raise HTTPException(
                status_code=500,
                detail=f"No resource defined for table {self._table_name}",
            )
        return resource

    @property
    def foreign_keys(self) -> list[dict]:
        foreign_keys = []
        for r in self.__relationships:
            related_model = r.mapper.class_
            foreign_model = related_model

            # Skip processing if the table name is 'evtp'
            if foreign_model.__tablename__ == "evtp":
                continue

            foreign_model_meta = TableMeta(
                table_name=foreign_model.__tablename__,
                db=self._db,
                recursion_level=self._recursion_level + 1,
                resource=self._resource,
            )

            foreign_table = config.resource.MAPPING_TABLE_TO_RESOURCE[foreign_model_meta._table_name]

            if foreign_table is None:
                raise HTTPException(
                    status_code=500,
                    detail=f"Foreign table {foreign_model_meta._table_name} not defined",
                )
            foreign_keys.append(
                {
                    "foreign_key": r.key,
                    "direction": str(r.direction),
                    "foreign_resource": foreign_table.resource,
                    "foreign_table": foreign_model_meta.summary,
                }
            )

        return foreign_keys

    def __get_required_optional_readonly_columns(self) -> dict:
        """
        Returns dict with required, optional and readonly columns.
        The lists are mutually exclusive: a union has all columns with no duplicates.
        """
        input_schema = self._table_mapping.input_schema
        all_columns = [c["column_name"] for c in self.__sql_columns]
        if input_schema is not None:
            schema = input_schema.schema()
            required_columns = schema.get("required", [])
            all_input_columns = schema["properties"].keys()
        else:
            required_columns = []
            all_input_columns = all_columns

        optional_columns = [c for c in all_input_columns if c not in required_columns]
        readonly_columns = [c for c in all_columns if c not in all_input_columns]

        return {
            "required": required_columns,
            "optional": optional_columns,
            "readonly": readonly_columns,
        }

    @property
    def fields(self):
        req_opt_ro_cols = self.__get_required_optional_readonly_columns()
        all_columns = functools.reduce(lambda a, b: a + b, req_opt_ro_cols.values())

        fields = {}
        for c in all_columns:
            sql_columns = [sql_column for sql_column in self.__sql_columns if sql_column["column_name"] == c]
            sql_column = sql_columns[0] if len(sql_columns) == 1 else None

            fields[c] = {
                "required": c in req_opt_ro_cols["required"],
                "optional": c in req_opt_ro_cols["optional"],
                "readonly": c in req_opt_ro_cols["readonly"],
                "max_length": sql_column["character_maximum_length"] if sql_column is not None else -1,
                "data_type": sql_column["data_type"] if sql_column is not None else -1,
            }

        # Manually add a field
        fields["evtp_upc"] = {
            "required": False,
            "optional": False,
            "readonly": True,
            "max_length": 11,
            "data_type": "integer",
        }
        return fields

    @property
    def summary(self):
        return {
            "resource": self.resource,
            "primary_key": self.primary_key,
            "description_key": self.description_key,
            "foreign_key_mapping": self.foreign_key_mapping,
            "foreign_keys": self.foreign_keys,
            "fields": self.fields,
        }


def get_model(resource: TableResource, db: Session) -> dict:
    table_name = config.resource.MAPPING_RESOURCE_TO_TABLE.get_table_name(resource)

    if table_name is not None:
        table_meta = TableMeta(table_name=table_name, db=db, resource=resource)
        return table_meta.summary
    else:
        raise ValueError(f"Resource {resource} not allowed.")

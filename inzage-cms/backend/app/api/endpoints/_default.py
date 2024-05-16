import importlib
import logging
import re
from types import ModuleType
from typing import Dict, Literal, Sequence, Type, Union

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import ScalarResult, exc, inspect
from sqlalchemy.ext.asyncio import AsyncSession

import app.crud as crud
import app.models as models
from app.api import exceptions
from app.database.database import Base, get_async_session
from app.models.evtp_acc import EvtpAcc

# Setup logger
logger = logging.getLogger(__name__)


def camelize(model_name: str) -> str:
    return re.sub(r"(?:^|_)(.)", lambda m: m.group(1).upper(), model_name)


def determine_if_relations_included(model_name: str, schema_module: ModuleType, schema_type: str) -> Type[BaseModel]:
    schema_class_name = f"{schema_type}"
    if hasattr(schema_module, schema_class_name):
        return getattr(schema_module, schema_class_name)
    else:
        return getattr(schema_module, f"{camelize(model_name)}")


def delete_relation_parent_child(router: APIRouter, base_model: Type[Base], *args) -> None:
    child_column = [attr for attr in dir(base_model) if attr.endswith("_cd_sub")][0]
    parent_column = [attr for attr in dir(base_model) if attr.endswith("_cd_sup")][0]

    @router.delete("/{child_cd}/parent/{parent_cd}")
    async def delete_relation_parent_child(
        child_cd: int,
        parent_cd: int,
        db: AsyncSession = Depends(get_async_session),
    ) -> Literal["DELETED", "NOT FOUND"]:
        """
        Delete the parent-child relation based on the given child code and parent code.

        Args:
            child_cd: The code of the child entity.
            parent_cd: The code of the parent entity.

        Returns:
        A string indicating the result of the deletion operation.
            "DELETED" if the relation was successfully deleted.
            "NOT FOUND" if the relation was not found.

        """
        result = await crud.struct.delete_relation_parent_child(
            db=db,
            base_model=base_model,
            child_column=child_column,
            parent_column=parent_column,
            child_cd=child_cd,
            parent_cd=parent_cd,
        )
        return result


def delete_attr(router, base_model, *args) -> None:
    @router.delete("/attribute/{attribute_name}/{primary_key_value}")
    async def delete_attr(
        attribute_name: str,
        primary_key_value: int,
        db: AsyncSession = Depends(get_async_session),
    ) -> Literal["DELETED", "NOT FOUND"]:
        """
        Clear an attribute from the base model by assigning a None value
        Args:
            attribute_name: which attribute of the base_model to clear
            primary_key_value: The cd code of primary_key

        Returns:
        A string indicating the result of the deletion operation.
            "DELETED" if the relation was successfully deleted.
            "NOT FOUND" if the relation was not found.
        """
        primary_key = inspect(base_model).primary_key[0].name

        result = await crud._default_crud_operations.delete_attr(
            db=db,
            base_model=base_model,
            primary_key=primary_key,
            primary_key_value=primary_key_value,
            attribute=attribute_name,
        )
        return result


def generate_router(
    model_name: str,
    base_model: Type[Base],
    additional_routes: list = [],
    filter_by_default: Dict[str, Union[str, bool, int]] = {},
) -> APIRouter:
    """
    Generate a router for the specified model.

    Args:
        model_name: The name of the model.
        base_mode: The base model class.
        additional_routes: Additional routes to be added to the router. Defaults to None.

    Returns: The generated router.
    """
    # Create router for functionalities
    router = APIRouter()

    schema_module = importlib.import_module(f"app.schemas.{model_name}")

    schema_with_relations = f"{camelize(model_name)}WithRelations"
    schema_minimal_list = f"{camelize(model_name)}MinimalList"
    schema_in = f"{camelize(model_name)}In"
    schema_base = f"{camelize(model_name)}"

    @router.get(
        "/",
        response_model=list[determine_if_relations_included(model_name, schema_module, schema_with_relations)],
    )
    async def get_all(
        *,
        db: AsyncSession = Depends(get_async_session),
    ) -> Sequence[Base] | ScalarResult[Base]:
        """
        Retrieve all records from the database. This is for viewing tables in the CMS.

        Returns: A list of records with the specified response model.
        """
        schema_type = "WithRelations" if hasattr(schema_module, schema_with_relations) else ""
        return await crud._default_crud_operations.get_all(
            db=db, base_model=base_model, schema_type=schema_type, filter_by_default=filter_by_default
        )

    @router.get("-list/", response_model=list[getattr(schema_module, schema_minimal_list)])
    async def get_list(
        *,
        db: AsyncSession = Depends(get_async_session),
    ) -> ScalarResult[Base]:
        """
        Retrieve a list of items. This is when opening a record which has foreign keys.

        Returns: A sequence of items.

        """
        return await crud._default_crud_operations.get_list(db=db, base_model=base_model)

    @router.get(
        "/filter/{search_query}",
        response_model=list[determine_if_relations_included(model_name, schema_module, schema_with_relations)],
    )
    async def get_filtered(
        *,
        search_query: str = "",
        db: AsyncSession = Depends(get_async_session),
        limit: int = Query(default=100, ge=1),
    ) -> Sequence[Base]:
        """
        Retrieve a list of filtered items.

        Args:
            search_query: The search query to filter the items. Defaults to "".
            limit: The maximum number of items to retrieve. Defaults to 100.

        Returns: A sequence of filtered items.
        """
        # Only include models that have many foreign keys and its primary use is to connect two tables
        if base_model in [
            models.evtp.EvtpGst,
            models.evtp_acc.EvtpAcc,
            models.evtp.EvtpOeComType,
            models.ond.EvtpOnd,
            models.gst.GstRge,
            models.gst.GstGg,
            models.gst.GstGstt,
            models.gg.GgEvtpSort,
            models.gg.GgStruct,
            models.oe.OeStruct,
        ]:
            return await crud._default_crud_operations.get_filtered(
                db=db,
                search_query=search_query,
                base_model=base_model,
                include_related_fields=True,
                filter_by_default=filter_by_default,
            )
        else:
            return await crud._default_crud_operations.get_filtered(
                db=db,
                search_query=search_query,
                base_model=base_model,
                include_related_fields=False,
                filter_by_default=filter_by_default,
            )

    @router.get(
        "/{primary_key}",
        response_model=determine_if_relations_included(model_name, schema_module, schema_with_relations),
    )
    async def get_one(
        primary_key: int,
        db: AsyncSession = Depends(get_async_session),
    ) -> Base | None:
        """
        Retrieve a single record from the database.

        Args:
            primary_key: The primary key of the record to retrieve.

        Returns: The retrieved record.
        """
        return await crud._default_crud_operations.get_one(db=db, base_model=base_model, primary_keys=[primary_key])

    @router.put(
        "/{primary_key}",
        response_model=determine_if_relations_included(model_name, schema_module, schema_with_relations),
    )
    async def update_one(
        body: getattr(schema_module, schema_in),  # type: ignore
        primary_key: int,
        db: AsyncSession = Depends(get_async_session),
        # current_gebruiker: schemas.gebruiker.Gebruiker = Depends(dependencies.get_current_gebruiker),
    ) -> Base | None:
        """
        Update a single record in the database.

        Args:
            body: The updated data for the record.
            primary_key: The primary key value of the record to be updated.
            current_gebruiker: The current user.

        Returns: The updated record.

        """
        return await crud._default_crud_operations.update_one(
            db=db, base_model=base_model, body=body, primary_key_value=primary_key, gebruiker="current_gebruiker.name"
        )

    @router.post("/", response_model=getattr(schema_module, schema_base))
    async def create_one(
        body: getattr(schema_module, schema_in),  # type: ignore
        db: AsyncSession = Depends(get_async_session),
        # current_gebruiker: schemas.gebruiker.Gebruiker = Depends(dependencies.get_current_gebruiker),
    ) -> EvtpAcc | Base:
        """
        Create a new record.

        Args:
            body: The request body containing the data for the new resource.
            current_gebruiker: The authenticated user.

        Returns: The created resource.

        Raises:
            HTTPException: If there is an error creating the resource.
        """
        if base_model == EvtpAcc:
            return await crud.evtp_acc.create_acc(db=db, body=body, gebruiker="current_gebruiker.name")
        return await crud._default_crud_operations.create_one(
            db=db, base_model=base_model, body=body, gebruiker="current_gebruiker.name"
        )

    @router.delete("/{primary_key}")
    async def delete_one(
        primary_key: int,
        db: AsyncSession = Depends(get_async_session),
    ) -> str:
        """
        Delete a record with the specified primary key.

        Args:
            primary_key: The primary key of the record to be deleted.

        Returns: A string indicating the success of the deletion operation.

        Raises: If there is a foreign key constraint violation.
        """
        try:
            if base_model == models.evtp_acc.EvtpAcc:
                return await crud.evtp_acc.delete_accordering(db=db, evtp_acc_cd=primary_key)
            else:
                return await crud._default_crud_operations.delete_one(
                    db=db, base_model=base_model, primary_key=primary_key
                )
        except exc.IntegrityError as e:
            logging.error(e)
            raise exceptions.ForeignKeyError()

    # Add additional routes
    if additional_routes:
        for additional_route in additional_routes:
            additional_route(router, base_model, model_name)

    return router

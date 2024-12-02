import logging
from datetime import datetime
from typing import Dict, List, Literal, Sequence, Type, Union

from pydantic import BaseModel
from pytz import timezone
from sqlalchemy import Boolean, DateTime, Float, Integer, Numeric, ScalarResult, String, and_, func, or_, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Load, aliased, joinedload, selectinload
from sqlalchemy.sql.elements import BooleanClauseList
from sqlalchemy.sql.expression import cast

from app import models
from app.api import exceptions
from app.config.resource import LIMIT_RESULTS_QUERY
from app.database.database import Base
from app.util.misc import create_upc

# Setup logger
logger = logging.getLogger(__name__)

entities_not_required_to_load = [
    "entities_evtp_ond",
    "entities_evtp_oe_com_type",
]


def _filter_on_column(
    base_model: Type[Base], filter_kwargs: Dict[str, Union[str, bool, int]] = {}
) -> List[BooleanClauseList]:
    conditions = []
    for key, original_value in filter_kwargs.items():
        col = getattr(base_model, key)
        column_type = col.type

        # Check the column type and cast the value accordingly
        if isinstance(column_type, String):
            cast_value = str(original_value)
        elif isinstance(column_type, Integer):
            cast_value = int(original_value)
        elif isinstance(column_type, Boolean):
            if isinstance(original_value, str) and original_value.lower() == "false":
                cast_value = False
            else:
                cast_value = bool(original_value)
        elif isinstance(column_type, DateTime):
            cast_value = original_value

        conditions.append(cast(col == cast_value, Boolean))
    return conditions


def _add_dynamic_joinedloads(
    base_model: Type[Base], model_relationship_tuples: List[tuple[Type[Base], Type[Base], str, str]]
) -> list[Load]:
    eager_loads = []
    for model, child_rel_model, parent_rel, child_rel in model_relationship_tuples:
        if issubclass(base_model, model):
            parent_entity = getattr(model, parent_rel)
            child_entity = getattr(child_rel_model, child_rel)
            eager_loads.append(joinedload(parent_entity, child_entity))
    return eager_loads


def _get_relationships(base_model: Type[Base]) -> list[str]:
    return [rel.key for rel in base_model.__mapper__.relationships if rel.key not in entities_not_required_to_load]


def _get_relationships_nested() -> List[tuple[Type[Base], Type[Base], str, str]]:
    """
    Get the nested relationships for a given base model.
    """
    return [
        (models.gg.Gg, models.gg.GgStruct, "parent_entities", "parent_entity"),
        (models.gg.Gg, models.gg.GgStruct, "child_entities", "child_entity"),
    ]


async def get_all(
    db: AsyncSession, base_model: Type[Base], schema_type: str, filter_by_default: Dict[str, Union[str, bool, int]] = {}
) -> Sequence[Base] | ScalarResult[Base]:
    """
    Gets all records for the given model. If the schema type is 'WithRelations', the relationships are also loaded.
    And conditions are applied on the query if filter_kwargs are provided.

    Args:
        base_model: The SQLAlchemy model class.
        schema_type: The Pydantic schema type (e.g., 'WithRelations').
    Returns: List of model instances.
    """
    relationships = _get_relationships(base_model=base_model)
    if hasattr(base_model, "ts_mut"):
        order_by_column = base_model.ts_mut.desc()  # type: ignore
    else:
        order_by_column = base_model.ts_acc.desc()  # type: ignore

    conditions = _filter_on_column(base_model=base_model, filter_kwargs=filter_by_default)

    if schema_type == "WithRelations":
        eager_loads = [joinedload(getattr(base_model, rel)) for rel in relationships]
        nested_relationships = _get_relationships_nested()
        eager_loads.extend(_add_dynamic_joinedloads(base_model, nested_relationships))
        stmt = (
            select(base_model)
            .options(*eager_loads)
            .filter(*conditions)
            .order_by(order_by_column)
            .limit(LIMIT_RESULTS_QUERY)
        )
        result = await db.execute(stmt)
        return result.unique().scalars().all()
    else:
        return await db.scalars(
            select(base_model).filter(*conditions).order_by(order_by_column).limit(LIMIT_RESULTS_QUERY)
        )


async def get_list(db: AsyncSession, base_model: Type[Base]) -> ScalarResult[Base]:
    """
    Retrieve a list of all records from the specified model.

    Args:
        base_model: The SQLAlchemy model to query.

    Returns: A list of all records from the specified model.
    """
    return await db.scalars(select(base_model).order_by(base_model.ts_mut.desc()))  # type: ignore


async def get_one(db: AsyncSession, base_model: Type[Base], primary_keys: list[int]) -> Base | None:
    """
    Retrieve a single record from the database based on the provided primary keys.

    Args:
        base_model: The SQLAlchemy model class.
        primary_keys: The list of primary key values.

    Returns: A list of instances of the model class matching the provided primary keys.
    """
    primary_key_column = base_model.__mapper__.primary_key[0]
    relationships = _get_relationships(base_model=base_model)

    eager_loads = [selectinload(getattr(base_model, rel)) for rel in relationships]
    nested_relationships = _get_relationships_nested()
    eager_loads.extend(_add_dynamic_joinedloads(base_model, nested_relationships))

    return await db.scalar(select(base_model).options(*eager_loads).filter(primary_key_column.in_(primary_keys)))


async def get_filtered(
    base_model: Type[Base],
    search_query: str,
    db: AsyncSession,
    include_related_fields: bool = False,
    filter_by_default: Dict[str, Union[str, bool, int]] = {},
) -> Sequence[Base]:
    """
    Retrieve filtered records from the database based on the search query.

    Args:
        base_model: The base model class.
        search_query: The search query to filter the records.
        limit: The maximum number of records to retrieve. Defaults to 100.

    Returns: A list of filtered records.

    """
    search_query = search_query.lower()
    stmt = select(base_model)

    # Build the where clause dynamically
    conditions = []
    search_fields = [c.key for c in base_model.__table__.columns]

    # Filter on the default fields
    default_condition = []
    default_condition = _filter_on_column(base_model=base_model, filter_kwargs=filter_by_default)

    # Search on the fields of the base model
    for field in search_fields:
        column = getattr(base_model, field)
        if not isinstance(column.type, (Integer, Float, Numeric, DateTime, Boolean)):
            conditions.append(cast(func.lower(column), String).contains(search_query))
        else:
            conditions.append(cast(column, String).contains(search_query))

    # Include specified fields from related models if requested
    if include_related_fields:
        fields_to_search = ["omschrijving", "gstt_naam", "tekst", "titel", "evtp_nm", "notitie"]
        for rel in base_model.__mapper__.relationships:
            related_model = rel.entity.class_
            for field in fields_to_search:
                column = getattr(related_model, field, None)
                if column is not None:
                    conditions.append(func.lower(column).contains(search_query))

    if conditions:
        stmt = stmt.where(or_(*conditions))

    # Order and limit the results
    if hasattr(base_model, "ts_mut"):
        stmt = stmt.order_by(base_model.ts_mut.desc()).limit(LIMIT_RESULTS_QUERY)  # type: ignore
    else:
        stmt = stmt.order_by(base_model.ts_acc.desc()).limit(LIMIT_RESULTS_QUERY)  # type: ignore

    # Eager load the relationships
    relationships = _get_relationships(base_model=base_model)
    eager_loads = [joinedload(getattr(base_model, rel)) for rel in relationships]
    nested_relationships = _get_relationships_nested()
    eager_loads.extend(_add_dynamic_joinedloads(base_model, nested_relationships))

    # Join the relationships
    oe_alias_1 = aliased(models.oe.Oe)
    oe_alias_2 = aliased(models.oe.Oe)
    gg_alias_1 = aliased(models.gg.Gg)
    gg_alias_2 = aliased(models.gg.Gg)
    stmt.join(oe_alias_1, onclause=models.gst.Gst.oe_best == oe_alias_1.oe_cd)
    stmt.join(oe_alias_2, onclause=models.gst.Gst.oe_bron == oe_alias_2.oe_cd)
    stmt.join(gg_alias_1, onclause=models.gg.GgStruct.gg_cd_sub == gg_alias_1.gg_cd)
    stmt.join(gg_alias_2, onclause=models.gg.GgStruct.gg_cd_sup == gg_alias_2.gg_cd)

    if base_model not in [models.gg.GgStruct, models.oe.OeKoepel, models.gst.Gst, models.oe.Oe, models.gg.Gg]:
        for rel in relationships:
            stmt = stmt.join(getattr(base_model, rel))

    result = await db.execute(stmt.options(*eager_loads).where(*default_condition))
    return result.unique().scalars().all()


async def update_one(
    db: AsyncSession,
    base_model: Type[Base],
    body: BaseModel,
    primary_key_value: int,
    gebruiker: str | None,
) -> Base | None:
    """
    Update a record by primary key.

    Args:
        model: The SQLAlchemy model class.
        body: The Pydantic model instance containing the updated data.
        primary_key_value: The value of the primary key column.
        gebruiker: The username of the user making the update.
    Returns: The updated model instance.
    """
    primary_key_column = base_model.__table__.primary_key.columns.values()[0]  # type: ignore
    relationships = _get_relationships(base_model=base_model)
    eager_loads = [selectinload(getattr(base_model, rel)) for rel in relationships]
    nested_relationships = _get_relationships_nested()
    eager_loads.extend(_add_dynamic_joinedloads(base_model, nested_relationships))

    payload = {
        **body.model_dump(exclude_unset=True),
        "user_nm": gebruiker,
    }
    if base_model != models.evtp_acc.EvtpAcc:
        payload.update({"ts_mut": datetime.now(tz=timezone("Europe/Amsterdam"))})

    async with db.begin():
        try:
            return await db.scalar(
                update(base_model)
                .filter(primary_key_column == primary_key_value)
                .values(payload)
                .execution_options(synchronize_session="fetch")
                .returning(base_model)
                .options(*eager_loads)
            )

        except IntegrityError as err:
            if "value violates unique constraint" in str(err):
                raise exceptions.UniqueViolation()
            else:
                logging.info(err)
                raise exceptions.UnprocessableEntity()

        except Exception as exc:
            logging.info(exc)
            raise exceptions.UnprocessableEntity()


async def create_one(db: AsyncSession, base_model: Type[Base], body: BaseModel, gebruiker: str | None) -> Base | None:
    """
    Create a new instance of the specified model in the database.

    Args:
        model: The model class.
        body: The data to be used for creating the instance.
        gebruiker: The name of the user creating the instance.

    Returns: The created instance.

    """
    payload = {
        **body.model_dump(exclude_unset=True),
        "ts_mut": datetime.now(tz=timezone("Europe/Amsterdam")),
        "ts_start": datetime.now(tz=timezone("Europe/Amsterdam")),
        "user_nm": gebruiker,
    }
    instance = base_model(**payload)

    # Check if model has a column named '_upc'
    column_upc = f"{base_model.__name__.lower()}_upc"
    try:
        async with db.begin():
            if hasattr(base_model, column_upc):
                list_gst_upc_object = await db.execute(select(getattr(base_model, column_upc)))
                gst_upc_object = list_gst_upc_object.scalars().all()

                while True:
                    gst_upc = create_upc()
                    if not gst_upc_object.__contains__(gst_upc):
                        payload[column_upc] = create_upc()
                        instance = base_model(**payload)
                        db.add(instance)
                        break
            else:
                db.add(instance)

        # Refresh the instance to get the generated primary key value
        await db.refresh(instance)
        return instance

    except IntegrityError as err:
        if "value violates unique constraint" in str(err):
            raise exceptions.UniqueViolation()


async def delete_one(db: AsyncSession, base_model: Type[Base], primary_key: int) -> str:
    """
    Delete a record from the database.

    Args:
        base_model: The base model class.
        primary_key: The primary key of the record to delete.

    Returns: A string indicating the result of the deletion. Possible values are "DELETED" if the record was deleted
    successfully, or "NOT FOUND" if the record was not found in the database.
    """
    async with db.begin():
        relation = await db.get(base_model, primary_key)
        if relation:
            await db.delete(relation)
            return "DELETED"
        else:
            return "NOT FOUND"


async def delete_attr(
    db: AsyncSession, base_model: Type[Base], primary_key: str, primary_key_value: int, attribute: str
) -> Literal["DELETED", "NOT FOUND"]:
    async with db.begin():
        stmt = await db.execute(
            select(base_model).filter(
                and_(
                    getattr(base_model, primary_key) == primary_key_value,
                )
            )
        )
        relation = stmt.scalar_one()
        if relation:
            setattr(relation, attribute, None)
            await db.commit()
            return "DELETED"
        else:
            return "NOT FOUND"

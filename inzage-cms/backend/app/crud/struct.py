from typing import Literal, Type

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import Base


async def delete_relation_parent_child(
    db: AsyncSession,
    base_model: Type[Base],
    child_column: str,
    parent_column: str,
    child_cd: int,
    parent_cd: int,
) -> Literal["DELETED", "NOT FOUND"]:
    async with db.begin():
        stmt = await db.execute(
            select(base_model).filter(
                and_(
                    getattr(base_model, child_column) == child_cd,
                    getattr(base_model, parent_column) == parent_cd,
                )
            )
        )
        relation = stmt.scalar_one()
        if relation:
            await db.delete(relation)
            return "DELETED"
        else:
            return "NOT FOUND"

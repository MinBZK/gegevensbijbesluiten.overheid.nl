from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import app.models as models


async def get_all_sup(db: AsyncSession) -> Sequence[models.gg.Gg]:
    subquery = select(models.gg.GgStruct.gg_cd_sup).scalar_subquery()
    result = await db.execute(select(models.gg.Gg).filter(models.gg.Gg.gg_cd.in_(subquery)))
    return result.scalars().unique().all()


async def get_all_sub(db: AsyncSession) -> Sequence[models.gg.Gg]:
    subquery = select(models.gg.GgStruct.gg_cd_sub).scalar_subquery()
    result = await db.execute(select(models.gg.Gg).filter(models.gg.Gg.gg_cd.in_(subquery)))
    return result.scalars().unique().all()

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import false, true

import app.models as models


async def get_all_sup(db: AsyncSession):
    result = await db.execute(select(models.gg.Gg).filter(models.gg.Gg.koepel == true()))
    return result.scalars().unique().all()


async def get_all_sub(db: AsyncSession):
    result = await db.execute(select(models.gg.Gg).filter(models.gg.Gg.koepel == false()))
    return result.scalars().unique().all()


async def get_all_sub_filtered(db: AsyncSession, gg_cd_sup: int):
    subquery = select(models.gg.GgStruct.gg_cd_sub).filter(models.gg.GgStruct.gg_cd_sup == gg_cd_sup).scalar_subquery()
    result = await db.execute(select(models.gg.Gg).filter(models.gg.Gg.gg_cd.in_(subquery)))
    return result.scalars().unique().all()

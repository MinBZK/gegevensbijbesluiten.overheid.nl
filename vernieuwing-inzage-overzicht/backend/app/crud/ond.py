import logging

from sqlalchemy import (
    and_,
    exists,
    select,
)
from sqlalchemy.orm import (
    Session,
    joinedload,
)

import app.models as models
from app.core.config import (
    CURRENT_VERSION,
    PUBLICATION_RANGE,
)

# Setup logger
logger = logging.getLogger(__name__)


def get_populated(db: Session, limit: int = 1000) -> list[models.ond.Ond]:
    """
    Gets onderwerpen which have at least one associated besluit.
    Returns: List of Ond object
    """
    ond = models.Ond
    stmt = exists().where(ond.entities_ond)
    return db.execute(select(ond).limit(limit).where(stmt).order_by(ond.sort_key)).scalars().all()


def get_one_with_evtps(db: Session, ond_cd: int):
    """
    Gets all onderwerpen based on a ond_cd.
    Returns: List of Ond object
    """
    evtp_ond = models.EvtpOnd
    evtp = models.EvtpVersion
    return (
        db.execute(
            select(evtp, evtp_ond)
            .join(
                evtp_ond,
                and_(
                    evtp.evtp_cd == evtp_ond.evtp_cd,
                    evtp_ond.ts_start >= evtp.ts_start,
                    evtp_ond.ts_start < evtp.ts_end,
                ),
            )
            .options(joinedload(evtp_ond.entity_evtp))
            .filter(
                and_(
                    evtp_ond.ond_cd == ond_cd,
                    evtp.id_publicatiestatus.in_(PUBLICATION_RANGE),
                    evtp.huidige_versie.in_(CURRENT_VERSION),
                )
            )
            .order_by(evtp.evtp_nm)
        )
        .unique()
        .scalars()
        .all()
    )

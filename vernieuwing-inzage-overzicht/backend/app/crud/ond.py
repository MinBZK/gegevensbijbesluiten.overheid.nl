import logging
from typing import Sequence

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


def get_populated(db: Session, limit: int = 1000) -> Sequence[models.ond.Ond]:
    """
    Gets onderwerpen which have at least one associated besluit.
    Returns: List of Ond object
    """
    ond = models.ond.Ond
    stmt = exists().where(ond.entities_ond)
    return db.execute(select(ond).limit(limit).where(stmt).order_by(ond.sort_key)).scalars().all()


def get_one_with_evtps(db: Session, ond_cd: int):
    """
    Gets all onderwerpen based on a ond_cd.
    Returns: List of Ond object
    """
    evtp_ond = models.ond.EvtpOnd
    model_evtp_version = models.evtp.EvtpVersion
    return (
        db.execute(
            select(model_evtp_version, evtp_ond)
            .join(
                evtp_ond,
                and_(
                    model_evtp_version.evtp_cd == evtp_ond.evtp_cd,
                    evtp_ond.ts_start >= model_evtp_version.ts_start,
                    evtp_ond.ts_start < model_evtp_version.ts_end,
                ),
            )
            .options(joinedload(evtp_ond.entity_evtp_version))
            .filter(
                and_(
                    evtp_ond.ond_cd == ond_cd,
                    model_evtp_version.id_publicatiestatus.in_(PUBLICATION_RANGE),
                    model_evtp_version.huidige_versie.in_(CURRENT_VERSION),
                )
            )
            .order_by(model_evtp_version.evtp_nm)
        )
        .unique()
        .scalars()
        .all()
    )

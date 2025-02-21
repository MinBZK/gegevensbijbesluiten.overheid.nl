import logging
from typing import Sequence

from sqlalchemy import (
    and_,
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
    Ond = models.ond.Ond
    EntityOnd = models.ond.EvtpOnd  # Assuming this is the association table or model

    # Subquery to check for associated entities
    subq = select(1).where(EntityOnd.ond_cd == Ond.ond_cd).exists()

    # Main query
    query = select(Ond).where(subq).order_by(Ond.sort_key).limit(limit)

    return db.execute(query).scalars().all()


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

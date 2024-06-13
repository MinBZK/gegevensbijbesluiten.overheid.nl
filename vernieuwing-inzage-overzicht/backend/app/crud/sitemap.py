from sqlalchemy import select
from sqlalchemy.orm import Session

import app.models as models
from app.core.config import (
    CURRENT_VERSION,
    PUBLICATION_RANGE,
    Pages,
)


def get_evtps(db: Session):
    model_evtp_version = models.evtp.EvtpVersion
    return (
        db.execute(
            select(model_evtp_version)
            .filter(
                model_evtp_version.id_publicatiestatus.in_(PUBLICATION_RANGE),
                model_evtp_version.huidige_versie.in_(CURRENT_VERSION),
            )
            .order_by(model_evtp_version.evtp_nm)
        )
        .scalars()
        .all()
    )


def get_urls(db: Session):
    """Fetch all possible urls"""
    endpoints_evtp_gst = []
    endpoints_gg = []
    sitemap_dict = []
    for evtp in get_evtps(db):
        sitemap_dict.append(
            {
                "loc": f"/besluit/{evtp.evtp_upc}",
                "lastmod": evtp.ts_mut,
                "changefreq": "daily",
            }
        )
        for gst in evtp.entities_evtp_gst:
            endpoints_evtp_gst.append(f"api/evtp-tree/{evtp.evtp_upc}/gst/{gst.entity_gst.gst_upc}")
            sitemap_dict.append(
                {
                    "loc": f"/{Pages.BESLUIT.value}/{evtp.evtp_upc}/{gst.entity_gst.gst_upc}",
                    "lastmod": gst.entity_gst.ts_mut,
                    "changefreq": "daily",
                }
            )
            for gg in gst.entities_gst_gg:
                endpoints_gg.append(f"api/gg/{gg.entity_gg_child.gg_upc}")
                sitemap_dict.append(
                    {
                        "loc": f"/{Pages.GEGEVENS.value}/{gg.entity_gg_child.gg_upc}",
                        "lastmod": gg.entity_gg_child.ts_mut,
                        "changefreq": "daily",
                    }
                )

    return (
        sitemap_dict,
        endpoints_evtp_gst,
        endpoints_gg,
    )

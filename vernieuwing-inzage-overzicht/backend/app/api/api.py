import logging

from fastapi import (
    APIRouter,
    Depends,
    Request,
)
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import crud
from app.api.endpoints import (
    evtp,
    evtp_tree,
    gg,
    oe,
    ond,
)
from app.database.database import (
    get_sync_session,
)

logging = logging.getLogger(__name__)


router = APIRouter()
router.include_router(
    evtp.router,
    prefix="/evtp",
    tags=["Besluit"],
)
router.include_router(
    evtp_tree.router,
    prefix="/evtp-tree",
    tags=["Besluit en onderliggende relaties"],
)
router.include_router(
    ond.router,
    prefix="/ond",
    tags=["Onderwerp"],
)
router.include_router(
    gg.router,
    prefix="/gg",
    tags=["Gegevens"],
)
router.include_router(
    oe.router,
    prefix="/oe",
    tags=["Organisaties"],
)


@router.get("/health-db")
def healthcheck_db(
    db: Session = Depends(get_sync_session),
) -> str:
    """
    check whether the database still responds
    """
    db.execute(select(1))  # random query
    return "OK"


@router.get("/health-backend")
def healthcheck_backend() -> str:
    """
    check whether the backend still responds
    """
    return "OK"


@router.get("/validation-each-url")
def validation_evtp_tree(
    request: Request,
    db: Session = Depends(get_sync_session),
) -> str:
    """
    Check whether each EVTP and the corresponding GST has data by sending a GET request to the endpoint of each EVTP.
    If the endpoint returns a 200 status code, the EVTP is considered healthy.
    Returns "OK" if all EVTPs are healthy.
    """
    # Check whether each EVTP has data
    base_url = request.base_url._url.replace("http://", "https://")  # Replace http with https
    logging.info(base_url)
    endpoint_checker = crud.test_all_evtps_data.EndpointChecker(base_url=base_url)
    (
        _,
        endpoints_evtp_gst,
        endpoints_gg,
    ) = crud.sitemap.get_urls(db)

    urls_evtp_gst = [f"{base_url}{evtp_upc}" for evtp_upc in endpoints_evtp_gst]
    urls_evtp_gg = [f"{base_url}{gg_upc}" for gg_upc in endpoints_gg]
    for endpoint in urls_evtp_gst:
        logging.info(f"Checking endpoint evtp-gst {endpoint}")
        endpoint_checker.check_endpoint(endpoint)

    for endpoint in urls_evtp_gg:
        logging.info(f"Checking endpoint gg {endpoint}")
        endpoint_checker.check_endpoint(endpoint)
    return "OK"


@router.get("/sitemap-urls")
def get_urls(
    db: Session = Depends(get_sync_session),
):
    """
    Retrieve a list of URLs for the generation of a sitemap.
    """
    (
        sitemap_dict,
        _,
        _,
    ) = crud.sitemap.get_urls(db)
    return sitemap_dict

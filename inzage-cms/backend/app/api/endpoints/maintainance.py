import asyncio
import ssl
from typing import Dict, List, Tuple

import httpx
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config.resource import MAPPING_RESOURCE_TO_TABLE, MAPPING_TABLE_TO_RESOURCE, URL_PER_RESOURCE, TableResource
from app.database.database import get_sync_session
from app.schemas.table import LinkStatus, ResourceLinkStatus

router = APIRouter()


async def check_link(client: httpx.AsyncClient, url: str, pk_value: int, desc_value: str) -> LinkStatus:
    """Check if a link is alive."""
    try:
        response = await client.get(url, follow_redirects=True, timeout=30.0)
        is_alive = response.status_code < 400
    except (httpx.HTTPError, asyncio.TimeoutError, ssl.SSLCertVerificationError, httpx.InvalidURL, ValueError):
        is_alive = False

    return LinkStatus(
        url=url,
        is_alive=is_alive,
        primary_key=pk_value,
        description=str(desc_value) if desc_value else "Koppeling",
    )


async def check_links_batch(client: httpx.AsyncClient, rows: List[Tuple]) -> List[LinkStatus]:
    """Check a batch of links concurrently."""
    tasks = []
    for row in rows:
        if len(row) == 3:
            pk_value, url, desc_value = row
        else:
            pk_value, url = row
            desc_value = None
        tasks.append(check_link(client, url, pk_value, desc_value or "Koppeling"))
    return await asyncio.gather(*tasks)


@router.get("/check-dead-links", response_model=ResourceLinkStatus)
async def check_dead_links(resource: TableResource, db: Session = Depends(get_sync_session)):
    """Check whether links are dead for a specific resource."""
    model = MAPPING_RESOURCE_TO_TABLE.get_model(resource.value)
    url_columns = URL_PER_RESOURCE.get(resource, [])

    if not model or not url_columns:
        return ResourceLinkStatus(resource=resource.value, links={})

    table_mapping = MAPPING_TABLE_TO_RESOURCE.get(model.__tablename__)
    if not table_mapping:
        return ResourceLinkStatus(resource=resource.value, links={})

    primary_key = table_mapping.primary_key
    description_key = table_mapping.description_key

    links: Dict[str, List[LinkStatus]] = {}
    async with httpx.AsyncClient(timeout=30.0, limits=httpx.Limits(max_connections=100)) as client:
        for column in url_columns:
            columns = [getattr(model, primary_key), getattr(model, column)]
            if description_key:
                columns.append(getattr(model, description_key))

            stmt = select(*columns).where(getattr(model, column).isnot(None)).distinct()
            rows = db.execute(stmt).fetchall()

            # Process links in batches
            batch_size = 50
            link_statuses = []
            for i in range(0, len(rows), batch_size):
                batch = rows[i : i + batch_size]
                link_statuses.extend(await check_links_batch(client, [tuple(row) for row in batch]))

            links[column] = link_statuses

    return ResourceLinkStatus(resource=resource.value, links=links)

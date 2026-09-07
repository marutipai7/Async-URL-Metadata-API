import httpx
import asyncio

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.metadata import MetaDataRequest, URLMetadata
from app.services.metadata_services import fetch_metadata
from app.services.database_service import (
    save_metadata,
    get_metadata_from_db,
)
from app.services.cache_service import (
    get_cached_metadata,
    cache_metadata,
)

router = APIRouter(
    prefix="/api",
    tags=["api"],
    responses={404: {"description": "Not found"}}
)


semaphore = asyncio.Semaphore(10)

async def fetch_with_limit(
        url:str,
        client: httpx.AsyncClient
):
    async with semaphore:
        return await fetch_metadata(
            url,
            client
        )

@router.post(
    "/metadata",
    response_model=list[URLMetadata]
)
async def get_metadata(
    request: MetaDataRequest,
    db: AsyncSession = Depends(get_db)
):

    results = []
    urls_to_fetch = []

    # Stage 1: Redis -> PostgreSQL
    for url_obj in request.urls:

        url = str(url_obj)

        cached_metadata = await get_cached_metadata(url)

        if cached_metadata:
            results.append(cached_metadata)
            continue

        database_metadata = await get_metadata_from_db(
            url,
            db
        )

        if database_metadata:

            await cache_metadata(database_metadata)

            results.append(database_metadata)
            continue

        urls_to_fetch.append(url)


    # Stage 2: Concurrent HTTP fetching
    if urls_to_fetch:

        limits = httpx.Limits(
            max_connections=20,
            max_keepalive_connections=10
        )

        timeout = httpx.Timeout(10.0)

        async with httpx.AsyncClient(
            limits=limits,
            timeout=timeout,
            follow_redirects=True
        ) as client:

            tasks = [
                fetch_with_limit(
                    url,
                    client
                )
                for url in urls_to_fetch
            ]

            fetched_results = await asyncio.gather(
                *tasks
            )


        # Stage 3: Save to PostgreSQL
        await save_metadata(
            fetched_results,
            db
        )


        # Stage 4: Save to Redis
        for metadata in fetched_results:
            await cache_metadata(metadata)


        results.extend(fetched_results)


    return results
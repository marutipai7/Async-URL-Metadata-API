import httpx
import asyncio
from app.db.database import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.metadata_services import fetch_metadata
from app.services.database_service import save_metadata
from app.schemas.metadata import MetaDataRequest, URLMetadata

router = APIRouter(
    prefix="/api",
    tags=["api"],
    responses={404: {"description": "Not found"}}
)


# @router.post("/metadata", response_model=URLMetadata)
# async def get_metadata(request: MetaDataRequest) -> URLMetadata:
#     # return await fetch_metadata(request.url[0])
#     url = str(request.urls[0])

#     metadata = await fetch_metadata(url)

#     return metadata

@router.post("/metadata", response_model=list[URLMetadata])
async def get_metadata(
    request: MetaDataRequest,
    db: AsyncSession = Depends(get_db)
    ):
    async with httpx.AsyncClient() as client:

        tasks = [
            fetch_metadata(str(url), client)
            for url in request.urls
        ]

        results = await asyncio.gather(*tasks)

    await save_metadata(
        metadata_items=results,
        db=db
        )

    return results
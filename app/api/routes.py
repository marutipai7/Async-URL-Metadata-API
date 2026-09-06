from fastapi import APIRouter
from app.schemas.metedata import MetaDataRequest, URLMetadata
from app.services.metedata_services import fetch_metadata
import httpx
import asyncio

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
async def get_metadata(request: MetaDataRequest):
    async with httpx.AsyncClient() as client:

        tasks = [
            fetch_metadata(str(url), client)
            for url in request.urls
        ]

        results = await asyncio.gather(*tasks)

        return results
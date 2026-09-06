import httpx
import logging
from bs4 import BeautifulSoup
from app.schemas.metadata import URLMetadata
from app.schemas.metadata import MetaDataRequest
from app.services.cache_service import cache_metadata, get_cached_metadata
logger = logging.getLogger(__name__)

# async def fetch_metadata(url:str) -> URLMetadata:

#     async with httpx.AsyncClient() as client:
#         response = await client.get(
#             url,
#             timeout=10.0,
#             follow_redirects=True
#         )

#     soup = BeautifulSoup(response.text, "html.parser")

#     title = None
#     description = None

#     # extract title
#     if soup.title and soup.title.string:
#         title = soup.title.string.strip()

#     # extract meta description
#     description_tag = soup.find(
#         "meta",
#         attrs={"name": "description"},
#     )

#     if description_tag:
#         description = description_tag.get("content")

#     return URLMetadata(
#         url=str(url),
#         title=title,
#         description=description,
#         status_code=response.status_code,
#         source=str(response.url),
#     )

async def fetch_metadata(
        url: str,
        client: httpx.AsyncClient) -> URLMetadata:

    cached_metadata = await get_cached_metadata(url)

    if cached_metadata:
        logger.info(
            "Cache HIT for URL: %s",
            url
        )

        return cached_metadata

    logger.info(
        "Cache MISS for URL: %s",
        url
    )

    try:
        response = await client.get(
            url,
            timeout=10.0,
            follow_redirects=True
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        title = None
        description = None

        if soup.title and soup.title.string:
            title = soup.title.string.strip()

        description_tag = soup.find(
            "meta",
            attrs={"name": "description"},
        )

        if description_tag:
            description = description_tag.get("content")

        metadata =  URLMetadata(
            url=str(url),
            title=title,
            description=description,
            status_code=response.status_code,
            source="fetched",
        )

        await cache_metadata(metadata)

        return metadata

    except httpx.TimeoutException:
        logger.warning(
            "Timeout while fetching url: %s",
            url
        )

        return URLMetadata(
            url= str(url),
            error="Request Timeout",
            source="error"
        )

    except httpx.RequestError as exc:
        logger.warning(
            "Error while fetching url %s: %s",
            url,
            exc
        )

    except Exception:
        logger.exception(
            "Unexpected error while fetching URL: %s",
            url
        )

        return  URLMetadata(
            url=str(url),
            error="Unexpected Error",
            source="error"
        )
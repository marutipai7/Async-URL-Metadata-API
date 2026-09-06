import httpx
from bs4 import BeautifulSoup
from app.schemas.metedata import URLMetadata
from app.schemas.metedata import MetaDataRequest
import logging

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

        return URLMetadata(
            url=str(url),
            title=title,
            description=description,
            status_code=response.status_code,
            source="fetched",
        )

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
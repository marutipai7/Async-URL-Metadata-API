import hashlib
import json

from app.db.redis import redis_client
from app.schemas.metadata import URLMetadata

CACHE_TTL = 3600

def create_cache_key(url:str) -> str:

    url_hash = hashlib.sha256(
        url.encode()
    ).hexdigest()

    return f"metadata:{url_hash}"

async def get_cached_metadata(
        url: str
) -> URLMetadata | None:

    key = create_cache_key(url)

    cached_data = await redis_client.get(key)

    if not cached_data:
        return None

    data = json.loads(cached_data)

    data["source"] = "cache"

    return URLMetadata(
        **data
    )

async def cache_metadata(
        metadata: URLMetadata
) -> None:

    if metadata.source == "error":
        return

    key = create_cache_key(metadata.url)

    data = metadata.model_dump()

    await redis_client.setex(
        key, 
        CACHE_TTL, 
        json.dumps(data))
from pydantic import BaseModel, HttpUrl

class MetaDataRequest(BaseModel):
    urls: list[HttpUrl]

class URLMetadata(BaseModel):
    url: str
    title: str | None = None
    description: str | None = None
    status_code: int | None = None
    source: str
    error: str | None = None
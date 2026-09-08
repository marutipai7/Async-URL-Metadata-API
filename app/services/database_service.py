from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.metadata import Metadata
from app.schemas.metadata import URLMetadata


async def save_metadata(
        metadata_items: list[URLMetadata],
        db: AsyncSession
    )-> None:


    for item in metadata_items:

        if item.source == "error":
            continue

        result = await db.execute(
            select(Metadata).where(
                Metadata.url == item.url
            )
        )

        existing_metadata = result.scalar_one_or_none()

        if existing_metadata:
            continue

        db_metadata = Metadata(
            url=item.url,
            title = item.title,
            description = item.description,
            status_code = item.status_code
        )

        db.add(db_metadata)

    await db.commit()


async def get_metadata_from_db(
        url:str,
        db:AsyncSession
) -> URLMetadata | None:

    result = await db.execute(
        select(Metadata).where(
            Metadata.url == url
        )
    )

    metadata = result.scalar_one_or_none()

    if not metadata:
        return None

    return URLMetadata(
        url=metadata.url,
        title=metadata.title,
        description=metadata.description,
        status_code=metadata.status_code,
        source="database"
    )
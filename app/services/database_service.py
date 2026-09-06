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


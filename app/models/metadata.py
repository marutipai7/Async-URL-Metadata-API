from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

class Base(DeclarativeBase):
    pass

class Metadata(Base):
    __tablename__ = "metadata"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    url: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True
    )

    title: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    description: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    status_code: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    # source: Mapped[str] = mapped_column(
    #     String,
    #     nullable=False
    # )

    # error: Mapped[str | None] = mapped_column(
    #     String,
    #     nullable=True
    # )
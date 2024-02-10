from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.settings import SQLITE_DB_PATH


class Base(DeclarativeBase):
    pass


class Url(Base):
    __tablename__ = "url"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str]


def setup_db() -> None:
    engine = create_engine(f"sqlite:///{SQLITE_DB_PATH}")
    Base.metadata.create_all(engine)

    return engine

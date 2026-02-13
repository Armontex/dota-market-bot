from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession


class Base(DeclarativeBase):
    pass


class Repository:

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

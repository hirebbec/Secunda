from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_base_session


class BaseDatabaseRepository:
    _session: AsyncSession

    def __init__(self, session: AsyncSession = Depends(get_base_session)) -> None:
        self._session = session

from typing import Optional

from sqlalchemy import create_engine
import sqlalchemy.exc
from sqlalchemy.orm import sessionmaker, Session

from settings import settings

engine = create_engine(
    "{}://{}:{}@{}:{}/{}".format(
        "postgresql",
        settings.DB_USER,
        settings.DB_PASSWORD,
        settings.DB_ADDR,
        settings.DB_PORT,
        settings.DB_NAME
    )
)

_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Database:
    def __init__(self, url: Optional[str] = None):
        if url is None:
            self._engine = engine
            self._maker = _session
        else:
            self._engine = create_engine(url)
            self._maker = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)

    def __enter__(self) -> Session:
        try:
            self._session = self._maker()
            return self._session
        except sqlalchemy.exc.TimeoutError:
            pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self._session.rollback()
        else:
            self._session.commit()
        self._session.close()
        self._session = None
        return False

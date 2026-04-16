from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from models.connection.interface.db_connection_handler import IDBConnectionHandler


class DBConnectionHandler(IDBConnectionHandler):
    def __init__(self) -> None:
        self.engine = create_engine(
            "sqlite:///./blog.db",
            connect_args={"check_same_thread": False},
        )
        self._session_factory = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )
        self._session: Session | None = None

    def __enter__(self):
        self._session = self._session_factory()
        return self._session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None and self._session:
            self._session.rollback()
        if self._session:
            self._session.close()

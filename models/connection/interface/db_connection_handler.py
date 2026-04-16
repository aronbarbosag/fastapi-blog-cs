from abc import ABC, abstractmethod

from sqlalchemy.orm import Session


class IDBConnectionHandler(ABC):
    @abstractmethod
    def __enter__(self) -> Session:
        raise NotImplementedError

    @abstractmethod
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object | None,
    ) -> None:
        raise NotImplementedError

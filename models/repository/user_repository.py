from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy import select

from models.connection.interface.db_connection_handler import IDBConnectionHandler
from models.entities.schemas import Post, User
from models.validators.schemas import UserUpdate


class UserRepository:
    def __init__(self, db_connection: IDBConnectionHandler) -> None:
        self.db_connection = db_connection

    def select_all(self):

        with self.db_connection as db:
            result = db.execute(select(User))
            result_proxy = result.scalars().all()

            return result_proxy

    def select_user(self, user_id: int):
        with self.db_connection as db:
            result = db.execute(select(User).where(User.id == user_id))
            result_proxy = result.scalars().first()

            return result_proxy

    def select_user_post(self, user_id: int):
        with self.db_connection as db:
            result = db.execute(select(Post).where(Post.user_id == user_id))
            result_proxy = result.scalars().all()

            return result_proxy

    def __search_existing_username(self, user: User):
        with self.db_connection as db:
            result = db.execute(select(User).where(User.username == user.username))

            existing_user = result.scalars().first()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists",
            )

    def __search_existing_email(self, user: User):
        with self.db_connection as db:
            result = db.execute(select(User).where(User.email == user.email))

            existing_user = result.scalars().first()

            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already exists",
                )

    def create_user(self, user: User):

        self.__search_existing_username(user)
        self.__search_existing_email(user)

        with self.db_connection as db:
            db.add(user)
            db.commit()
            db.refresh(user)

        return user

    def update_user(self, user_id: int, user_image_file: UserUpdate):

        with self.db_connection as db:
            user = db.get(User, user_id)

            user_data_receive = user_image_file.model_dump(exclude_unset=True)

            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_BAD_REQUEST,
                    detail="User id not found",
                )

            for key, value in user_data_receive.items():
                setattr(user, key, value)

            db.commit()
            db.refresh(user)

        return user

    def delete_user(self, user_id: int):

        user = self.select_user(user_id)

        if not user:
            return None

        with self.db_connection as db:
            user_ = db.merge(user)
            db.delete(user_)
            db.commit()

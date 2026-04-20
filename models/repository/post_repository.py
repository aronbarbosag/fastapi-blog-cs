from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy import select

from models.connection.interface.db_connection_handler import IDBConnectionHandler
from models.entities.schemas import Post, User
from models.validators.schemas import PostUpdate


class PostRepository:
    def __init__(self, db_connection: IDBConnectionHandler) -> None:
        self.db_connection = db_connection

    def select_all(self):

        with self.db_connection as db:
            result = db.execute(select(Post))
            result_proxy = result.scalars().all()

            return result_proxy

    def select_post(self, post_id: int):
        with self.db_connection as db:
            result = db.execute(select(Post).where(Post.id == post_id))
            result_proxy = result.scalars().first()

            return result_proxy

    def __search_existing_user(self, post: Post):
        with self.db_connection as db:
            result = db.execute(select(User).where(User.id == post.user_id))

            existing_user = result.scalars().first()

            if not existing_user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found",
                )

    def __search_existing_post(self, post_id: int):
        with self.db_connection as db:
            result = db.execute(select(Post).where(Post.id == post_id))

            existing_post = result.scalars().first()

            if not existing_post:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Post not found",
                )
            return existing_post

    def create_post(self, post: Post):

        self.__search_existing_user(post)

        with self.db_connection as db:
            db.add(post)
            db.commit()
            db.refresh(post)

        return post

    def delete_post(self, post_id: int):

        post = self.__search_existing_post(post_id)

        with self.db_connection as db:
            post_ = db.merge(post)
            db.delete(post_)
            db.commit()

    def update_post(self, post_id: int, post_data_to_update: PostUpdate):

        data = post_data_to_update.model_dump(exclude_unset=True)
        post = self.__search_existing_post(post_id)

        with self.db_connection as db:
            post_ = db.merge(post)

            for key, value in data.items():
                setattr(post_, key, value)
            db.commit()
            db.refresh(post_)
        return post_

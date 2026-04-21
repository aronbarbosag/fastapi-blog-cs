from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import JSONResponse

from models.connection.db_connection_handler import DBConnectionHandler
from models.entities.schemas import User
from models.repository.user_repository import UserRepository
from models.validators.schemas import (
    PostResponse,
    UserCreate,
    UserResponse,
    UserUpdate,
)

from .templates import templates

router = APIRouter()


@router.post(
    "/api/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["users"],
)
def create_user(user: UserCreate):
    """Create a user for make an post"""

    connection = DBConnectionHandler()
    repo = UserRepository(connection)

    new_user = User(username=user.username, email=user.email)

    user_created = repo.create_user(new_user)

    return user_created


@router.get("/api/users", response_model=list[UserResponse], tags=["users"])
def get_users():
    """Get all users"""

    connection = DBConnectionHandler()
    repo = UserRepository(connection)

    users = repo.select_all()

    if users:
        return users

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.get("/api/users/{user_id}", response_model=UserResponse, tags=["users"])
def get_user(user_id: int):
    """Get a user"""
    connection = DBConnectionHandler()
    repo = UserRepository(connection)

    user = repo.select_user(user_id=user_id)

    if user:
        return user

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.get(
    "/api/users/{user_id}/posts",
    response_model=list[PostResponse],
    tags=["users", "posts"],
)
def get_user_posts(user_id: int):
    """Get user's posts"""

    connection = DBConnectionHandler()
    repo = UserRepository(connection)

    posts = repo.select_user_post(user_id=user_id)

    return posts


@router.put(
    "/api/users/{id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    tags=["users"],
)
def update_user(user_id: int, data: UserUpdate):
    """Update user's information"""

    connection = DBConnectionHandler()
    repo = UserRepository(connection)

    post = repo.update_user(user_id=user_id, user_image_file=data)

    return post


@router.get("/users/{user_id}/posts", include_in_schema=False, name="user_posts")
def user_posts_page(request: Request, user_id: int):

    connection = DBConnectionHandler()
    repo = UserRepository(connection)

    posts = repo.select_user_post(user_id)
    user = repo.select_user(user_id)
    if posts and user:
        return templates.TemplateResponse(
            request,
            "user_posts.html",
            {"posts": posts, "user": user, "title": f"{user.username}'s Posts"},
        )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.delete("/api/users/{id}", status_code=status.HTTP_200_OK, tags=["users"])
def delete_user(id: int):
    """Delete  an  post"""
    connection = DBConnectionHandler()
    repo = UserRepository(connection)

    repo.delete_user(id)

    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"detail": "Succefully Delete"}
    )

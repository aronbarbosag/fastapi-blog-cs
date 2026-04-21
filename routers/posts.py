from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import JSONResponse

from models.connection.db_connection_handler import DBConnectionHandler
from models.entities.schemas import Post
from models.repository.post_repository import PostRepository
from models.validators.schemas import (
    PostCreate,
    PostResponse,
    PostUpdate,
)

from .templates import templates

router = APIRouter()


@router.get("/", include_in_schema=False, name="home")
@router.get("/posts", include_in_schema=False, name="posts")
def home(request: Request):

    connection = DBConnectionHandler()
    repo = PostRepository(connection)
    posts = repo.select_all()

    return templates.TemplateResponse(
        request, "home.html", {"posts": posts, "title": "Home"}
    )


@router.get("/posts/{id}", include_in_schema=False, name="post_html")
def get_post_html(request: Request, id: int):

    connection = DBConnectionHandler()
    repo = PostRepository(connection)
    post = repo.select_post(post_id=id)

    if post:
        title = post.title[:50]
        return templates.TemplateResponse(
            request,
            "post.html",
            {"post": post, "title": title},
        )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


@router.get("/api/posts", response_model=list[PostResponse], tags=["posts"])
def get_posts():
    """Get all posts"""

    connection = DBConnectionHandler()
    repo = PostRepository(connection)

    posts = repo.select_all()

    return posts


@router.get("/api/posts/{id}", response_model=PostResponse, tags=["posts"])
def get_post(post_id: int):
    """Get a single post"""

    connection = DBConnectionHandler()
    repo = PostRepository(connection)

    post = repo.select_post(post_id=post_id)

    if post:
        return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


@router.put(
    "/api/posts/{id}",
    response_model=PostResponse,
    status_code=status.HTTP_200_OK,
    tags=["posts"],
)
def update_post(post_id: int, data: PostUpdate):
    """update an  post"""

    connection = DBConnectionHandler()
    repo = PostRepository(connection)

    post = repo.update_post(post_id=post_id, post_data_to_update=data)

    return post


@router.post("/api/posts", status_code=status.HTTP_201_CREATED, tags=["posts"])
def create_post(post: PostCreate):
    """Create an  post"""
    connection = DBConnectionHandler()
    repo = PostRepository(connection)

    new_post = Post(title=post.title, content=post.content, user_id=post.user_id)
    new_post_response = repo.create_post(new_post)

    return new_post_response


@router.delete("/api/posts/{id}", status_code=status.HTTP_200_OK, tags=["posts"])
def delete_post(id: int):
    """Delete  an  post"""
    connection = DBConnectionHandler()
    repo = PostRepository(connection)

    repo.delete_post(id)

    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"detail": "Succefully Delete"}
    )

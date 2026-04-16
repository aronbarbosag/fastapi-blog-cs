from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError

# from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException as StarletteHTTPException

from database import Base, engine, get_db
from models.connection.db_connection_handler import DBConnectionHandler
from models.entities.schemas import Post, User
from models.repository.post_repository import PostRepository
from models.repository.user_repository import UserRepository
from models.validators.schemas import PostCreate, PostResponse, UserCreate, UserResponse

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.mount("/media", StaticFiles(directory="media"), name="media")

templates = Jinja2Templates(directory="templates")


@app.get("/", include_in_schema=False, name="home")
@app.get("/posts", include_in_schema=False, name="posts")
def home(request: Request):

    connection = DBConnectionHandler()
    repo = PostRepository(connection)
    posts = repo.select_all()

    return templates.TemplateResponse(
        request, "home.html", {"posts": posts, "title": "Home"}
    )


@app.get("/posts/{id}", include_in_schema=False, name="post_html")
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


@app.get("/users/{user_id}/posts", include_in_schema=False, name="user_posts")
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


@app.post(
    "/api/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def create_user(user: UserCreate):

    connection = DBConnectionHandler()
    repo = UserRepository(connection)

    new_user = User(username=user.username, email=user.email)

    user_created = repo.create_user(new_user)

    return user_created


@app.get("/api/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):

    connection = DBConnectionHandler()
    repo = UserRepository(connection)

    user = repo.select_user(user_id=user_id)

    if user:
        return user

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@app.get("/api/users/{user_id}/posts", response_model=list[PostResponse])
def get_user_posts(user_id: int):

    connection = DBConnectionHandler()
    repo = UserRepository(connection)

    posts = repo.select_user_post(user_id=user_id)

    return posts


@app.get("/api/posts", response_model=list[PostResponse])
def get_posts():

    connection = DBConnectionHandler()
    repo = PostRepository(connection)

    posts = repo.select_all()

    return posts


@app.get("/api/posts/{id}", response_model=PostResponse)
def get_post(post_id: int, db: Annotated[Session, Depends(get_db)]):

    connection = DBConnectionHandler()
    repo = PostRepository(connection)

    post = repo.select_post(post_id=post_id)

    if post:
        return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


@app.post("/api/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate):
    connection = DBConnectionHandler()
    repo = PostRepository(connection)

    new_post = Post(title=post.title, content=post.content, user_id=post.user_id)
    new_post_response = repo.create_post(new_post)

    return new_post_response


@app.delete("/api/posts/{id}", status_code=status.HTTP_200_OK)
def delete_post(id: int):

    connection = DBConnectionHandler()
    repo = PostRepository(connection)

    repo.delete_post(id)

    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"detail": "Succefully Delete"}
    )


## StarletteHTTPException Handler
@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An error occurred. Please check your request and try again."
    )

    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
        )
    return templates.TemplateResponse(
        request,
        "404.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code,
    )


### RequestValidationError Handler
@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exception.errors()},
        )
    return templates.TemplateResponse(
        request,
        "404.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": "Invalid request. Please check your input and try again.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )

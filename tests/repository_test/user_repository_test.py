from models.connection.db_connection_handler import DBConnectionHandler
from models.repository.user_repository import UserRepository


def test_select_all():
    connection = DBConnectionHandler()
    repo = UserRepository(connection)

    result = repo.select_all()
    print(result)


def test_select_user_post():
    connection = DBConnectionHandler()
    repo = UserRepository(connection)

    result = repo.select_user_post(user_id=2)
    print(result)


# def test_create_user():
#     connection = DBConnectionHandler()
#     repo = UserRepository(connection)

#     new_user = User()

#     result = repo.create_user()
#     print(result)

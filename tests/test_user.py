import logging
from datetime import datetime

import pytz
from sqlalchemy import delete, insert, select
from sqlalchemy.orm import sessionmaker
from starlette import status

from ..src.endpoints.auth import get_password_hash
from ..src.models.all_models import User
from .client import client

NOT_AUTH = {"detail": "Not authenticated"}
LIB_USER = {
    "email": "user@super.com",
    "username": "super_user",
    "password": get_password_hash("12345678"),
    "first_name": "Users First name",
    "last_name": "Users last name",
    "contact_number": "users cellphone number",
    "address": "users physical address",
    "is_librarian": True,
    "is_active": True,
    "date_of_joining": datetime.now(pytz.UTC),
}
TEST_USER = {
    "email": "user1@gmail.com",
    "username": "user1",
    "password": get_password_hash("12345678"),
    "first_name": "Users First name",
    "last_name": "Users last name",
    "contact_number": "users cellphone number",
    "address": "users physical address",
    "is_librarian": False,
    "is_active": True,
    "date_of_joining": datetime.now(pytz.UTC),
}


def test_get_all_users(test_db: sessionmaker) -> None:
    check_no_auth()
    token = get_fresh_token(test_db)
    new_user = User(**TEST_USER)
    insert_user(test_db, new_user)
    response = client.get("/user/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2
    assert response.json()[0].get("username") == LIB_USER.get("username")
    assert response.json()[1].get("username") == TEST_USER.get("username")


def test_get_user_by_id(test_db: sessionmaker) -> None:
    check_no_auth()
    token = get_fresh_token(test_db)
    new_user = User(**TEST_USER)
    insert_user(test_db, new_user)
    response = client.get("/user/2", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("username") == "user1"

    response = client.get("/user/3", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_404_NOT_FOUND


# Helper functions


def check_no_auth() -> None:
    """
    Hit the url with no token to check response
    """
    response = client.get("/user/")
    assert response.json() == NOT_AUTH
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def remove_all_users(test_db: sessionmaker) -> None:
    """
    Removes all the users from the database.
    """
    with test_db() as db:
        db.execute(delete(User).where(True))
        db.commit()


def insert_user(test_db: sessionmaker, user: User) -> None:
    """
    Creates a user in database
    """
    with test_db() as db:
        db.add(user)
        db.commit()


def get_fresh_token(db: sessionmaker) -> str:
    """
    Clears the db, create new librarian and returns its jwt token
    """
    remove_all_users(db)
    new_user = User(**LIB_USER)
    insert_user(db, new_user)
    jwt_token = (
        client.post(
            "/auth/token",
            data={"username": "super_user", "password": "12345678"},
        )
        .json()
        .get("token")
    )
    return jwt_token
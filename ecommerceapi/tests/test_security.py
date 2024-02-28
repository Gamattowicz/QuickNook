import pytest
from jose import jwt

from ecommerceapi import security


def test_access_token_expire_minutes():
    assert security.access_token_expire_minutes() == 30


def test_confirm_token_expire_minutes():
    assert security.confirm_token_expire_minutes() == 1440


def test_create_access_token():
    token = security.create_access_token("123", "client")
    assert {"sub": "123", "type": "access", "role": "client"}.items() <= jwt.decode(
        token, key=security.SECRET_KEY, algorithms=[security.ALGORITHM]
    ).items()


def test_create_confirm_token():
    token = security.create_confirmation_token("123", "client")
    assert {
        "sub": "123",
        "type": "confirmation",
        "role": "client",
    }.items() <= jwt.decode(
        token, key=security.SECRET_KEY, algorithms=[security.ALGORITHM]
    ).items()


def test_get_subject_for_token_type_valid_confirmation():
    email = "test@example.com"
    role = "client"
    token = security.create_confirmation_token(email, role)
    assert email == security.get_subject_for_token_type(token, "confirmation")


def test_get_subject_for_token_type_valid_access():
    email = "test@example.com"
    role = "client"
    token = security.create_access_token(email, role)
    assert email == security.get_subject_for_token_type(token, "access")


def test_get_subject_for_token_type_expired(mocker):
    mocker.patch("ecommerceapi.security.access_token_expire_minutes", return_value=-1)
    email = "test@example.com"
    role = "client"
    token = security.create_access_token(email, role)
    with pytest.raises(security.HTTPException) as exc_info:
        security.get_subject_for_token_type(token, "access")
    assert "Token has expired" == exc_info.value.detail


def test_get_subject_for_token_type_invalid_token():
    token = "Invalid token"
    with pytest.raises(security.HTTPException) as exc_info:
        security.get_subject_for_token_type(token, "access")
    assert "Invalid token" == exc_info.value.detail


def test_get_subject_for_token_type_missing_sub():
    email = "test@example.com"
    role = "client"
    token = security.create_access_token(email, role)
    payload = jwt.decode(
        token, key=security.SECRET_KEY, algorithms=[security.ALGORITHM]
    )
    del payload["sub"]
    token = jwt.encode(payload, key=security.SECRET_KEY, algorithm=security.ALGORITHM)

    with pytest.raises(security.HTTPException) as exc_info:
        security.get_subject_for_token_type(token, "access")
    assert "Token is missing 'sub' field" == exc_info.value.detail


def test_get_subject_for_token_type_wrong_type():
    email = "test@example.com"
    role = "client"
    token = security.create_confirmation_token(email, role)
    with pytest.raises(security.HTTPException) as exc_info:
        security.get_subject_for_token_type(token, "access")
    assert "Token has incorrect type, expected 'access'" == exc_info.value.detail


def test_password_hashes():
    password = "password"
    assert security.verify_password(password, security.get_password_hash(password))


@pytest.mark.anyio
async def test_get_user(registered_user: dict):
    user = await security.get_user(registered_user["email"])

    assert user.email == registered_user["email"]


@pytest.mark.anyio
async def test_get_user_not_found():
    user = await security.get_user("test2@example.com")

    assert user is None


@pytest.mark.anyio
async def test_authenticate_user(confirmed_user: dict):
    user = await security.authenticate_user(
        confirmed_user["email"], confirmed_user["password"]
    )

    assert user.email == confirmed_user["email"]


@pytest.mark.anyio
async def test_authenticate_user_with_role(confirmed_user: dict):
    user = await security.authenticate_user_with_role(
        confirmed_user["email"], confirmed_user["password"], confirmed_user["role"]
    )

    assert user.email == confirmed_user["email"]
    assert user.role == confirmed_user["role"]


@pytest.mark.anyio
async def test_authenticate_user_not_found():
    with pytest.raises(security.HTTPException):
        await security.authenticate_user("test3@example.com", "123456")


@pytest.mark.anyio
async def test_authenticate_user_wrong_password(registered_user: dict):
    with pytest.raises(security.HTTPException):
        await security.authenticate_user(registered_user["email"], "bad_password")


@pytest.mark.anyio
async def test_authenticate_user_with_wrong_role(confirmed_user: dict):
    with pytest.raises(security.HTTPException):
        await security.authenticate_user_with_role(
            confirmed_user["email"], confirmed_user["password"], "seller"
        )


@pytest.mark.anyio
async def test_get_current_user(registered_user: dict):
    token = security.create_access_token(
        registered_user["email"], registered_user["role"]
    )
    user = await security.get_current_user(token)
    assert user.email == registered_user["email"]


@pytest.mark.anyio
async def test_get_current_user_invalid_token():
    with pytest.raises(security.HTTPException):
        await security.get_current_user("Invalid token")


@pytest.mark.anyio
async def test_current_user_wrong_type_token(registered_user: dict):
    token = security.create_confirmation_token(
        registered_user["email"], registered_user["role"]
    )

    with pytest.raises(security.HTTPException):
        await security.get_current_user(token)

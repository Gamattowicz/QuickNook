import logging

from fastapi import APIRouter, BackgroundTasks, HTTPException, Request, status

from api import tasks
from api.database import database, user_table
from api.models.user import UserIn
from api.security import (
    authenticate_user,
    create_access_token,
    create_confirmation_token,
    get_password_hash,
    get_subject_for_token_type,
    get_user,
)

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/register", status_code=201)
async def register(user: UserIn, background_tasks: BackgroundTasks, request: Request):
    if await get_user(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with that email already exists",
        )

    hashed_password = get_password_hash(user.password)
    query = user_table.insert().values(
        email=user.email, password=hashed_password, role=user.role
    )

    logger.debug(query)

    await database.execute(query)
    background_tasks.add_task(
        tasks.send_user_registration_email,
        user.email,
        confirmation_url=request.url_for(
            "confirm_email", token=create_confirmation_token(user.email, user.role)
        ),
    )
    return {
        "detail": "User created. Please confirm your email.",
        "confirmation_url": request.url_for(
            "confirm_email", token=create_confirmation_token(user.email, user.role)
        ),
    }


@router.post("/token")
async def login(user: UserIn):
    user = await authenticate_user(user.email, user.password)
    access_token = create_access_token(user.email, user.role)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/confirm/{token}")
async def confirm_email(token: str):
    email = get_subject_for_token_type(token, "confirmation")
    query = (
        user_table.update().where(user_table.c.email == email).values(confirmed=True)
    )

    logger.debug(query)

    await database.execute(query)
    return {"detail": "User confirmed"}

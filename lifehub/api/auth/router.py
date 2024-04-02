from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from .lib import CredentialsException, authenticate_user, create_access_token, users_db
from .schemas import Token

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/token", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(users_db, form_data.username, form_data.password)
    if not user:
        raise CredentialsException()
    expires_delta = timedelta(days=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=expires_delta
    )
    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=expires_delta.total_seconds(),
    )

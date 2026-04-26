from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
from schemas.user import UserCreate, UserResponse, UserLogin, Token
from crud.user import create_user, get_user_by_username, get_user_by_email
from auth.security import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrasi User Baru"
)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Registrasi user baru.

    - **username**: Harus unik, minimal 3 karakter
    - **email**: Harus unik
    - **password**: Minimal 6 karakter
    """
    # Cek apakah username sudah ada
    existing_user = get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Username '{user_data.username}' already registered"
        )

    # Cek apakah email sudah ada
    existing_email = get_user_by_email(db, user_data.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Email '{user_data.email}' already registered"
        )

    # Buat user baru
    new_user = create_user(db, user_data.username, user_data.email, user_data.password)
    return new_user


@router.post(
    "/login",
    response_model=Token,
    summary="Login & Dapatkan Token JWT (Form)"
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login dengan username dan password (OAuth2 form).

    Endpoint ini kompatibel dengan tombol **Authorize** di Swagger UI.
    Masukkan username dan password, lalu klik Authorize.

    Mengembalikan JWT access token.
    """
    # Cari user berdasarkan username
    user = get_user_by_username(db, form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verifikasi password
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")


@router.post(
    "/login/json",
    response_model=Token,
    summary="Login & Dapatkan Token JWT (JSON)"
)
def login_json(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    Login dengan JSON body (untuk Postman / frontend).

    - **username**: Username yang terdaftar
    - **password**: Password user
    """
    user = get_user_by_username(db, user_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")


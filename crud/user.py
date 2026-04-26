from sqlalchemy.orm import Session

from models.user import User
from auth.security import hash_password


def get_user_by_username(db: Session, username: str):
    """Cari user berdasarkan username."""
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str):
    """Cari user berdasarkan email."""
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int):
    """Cari user berdasarkan ID."""
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, username: str, email: str, password: str):
    """Buat user baru dengan password yang sudah di-hash."""
    hashed = hash_password(password)
    db_user = User(
        username=username,
        email=email,
        hashed_password=hashed
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

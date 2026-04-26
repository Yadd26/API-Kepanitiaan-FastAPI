from typing import Optional

from sqlalchemy.orm import Session

from models.event import Event
from schemas.event import EventCreate, EventUpdate


def create_event(db: Session, event_data: EventCreate, user_id: int):
    """Buat event baru."""
    db_event = Event(
        title=event_data.title,
        description=event_data.description,
        location=event_data.location,
        event_date=event_data.event_date,
        created_by=user_id
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def get_events(db: Session, skip: int = 0, limit: int = 100):
    """Ambil semua event dengan pagination."""
    return db.query(Event).offset(skip).limit(limit).all()


def get_event(db: Session, event_id: int):
    """Ambil detail satu event berdasarkan ID."""
    return db.query(Event).filter(Event.id == event_id).first()


def update_event(db: Session, event_id: int, event_data: EventUpdate):
    """Update event yang sudah ada."""
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if not db_event:
        return None

    update_data = event_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_event, field, value)

    db.commit()
    db.refresh(db_event)
    return db_event


def delete_event(db: Session, event_id: int):
    """Hapus event berdasarkan ID. Mengembalikan True jika berhasil."""
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if not db_event:
        return False
    db.delete(db_event)
    db.commit()
    return True

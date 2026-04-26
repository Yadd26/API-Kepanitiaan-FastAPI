from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models.user import User
from schemas.event import EventCreate, EventUpdate, EventResponse, EventListResponse
from crud.event import (
    create_event,
    get_events,
    get_event,
    update_event,
    delete_event,
)
from auth.security import get_current_user

router = APIRouter(
    prefix="/events",
    tags=["Events"]
)


@router.post(
    "/",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Buat Event Baru"
)
def create_new_event(
    event_data: EventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Buat event kepanitiaan baru. **Memerlukan autentikasi JWT.**

    - **title**: Nama kegiatan (wajib)
    - **description**: Deskripsi kegiatan
    - **location**: Lokasi kegiatan
    - **event_date**: Tanggal/waktu kegiatan (format ISO 8601)
    """
    return create_event(db, event_data, current_user.id)


@router.get(
    "/",
    response_model=List[EventListResponse],
    summary="Lihat Semua Event"
)
def read_events(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Ambil daftar semua event kepanitiaan.
    Mendukung pagination dengan parameter `skip` dan `limit`.
    """
    return get_events(db, skip=skip, limit=limit)


@router.get(
    "/{event_id}",
    response_model=EventResponse,
    summary="Detail Event"
)
def read_event(event_id: int, db: Session = Depends(get_db)):
    """
    Ambil detail satu event berdasarkan ID, termasuk daftar task-nya.
    """
    db_event = get_event(db, event_id)
    if not db_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id {event_id} not found"
        )
    return db_event


@router.put(
    "/{event_id}",
    response_model=EventResponse,
    summary="Update Event"
)
def update_existing_event(
    event_id: int,
    event_data: EventUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update data event. **Hanya creator event yang bisa mengupdate.**

    Semua field bersifat opsional — hanya field yang dikirim yang akan diupdate.
    """
    # Cek event ada
    db_event = get_event(db, event_id)
    if not db_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id {event_id} not found"
        )

    # Cek apakah current user adalah creator
    if db_event.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not the creator of this event"
        )

    updated = update_event(db, event_id, event_data)
    return updated


@router.delete(
    "/{event_id}",
    status_code=status.HTTP_200_OK,
    summary="Hapus Event"
)
def delete_existing_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Hapus event beserta semua task-nya. **Hanya creator event yang bisa menghapus.**
    """
    # Cek event ada
    db_event = get_event(db, event_id)
    if not db_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id {event_id} not found"
        )

    # Cek apakah current user adalah creator
    if db_event.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not the creator of this event"
        )

    delete_event(db, event_id)
    return {"message": f"Event '{db_event.title}' has been deleted successfully"}

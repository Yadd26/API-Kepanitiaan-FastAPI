from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models.user import User
from schemas.task import TaskCreate, TaskUpdate, TaskResponse
from crud.task import (
    create_task,
    get_tasks,
    get_tasks_by_event,
    get_task,
    update_task,
    delete_task,
)
from crud.event import get_event
from auth.security import get_current_user

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Buat Task Baru"
)
def create_new_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Buat task kepanitiaan baru. **Memerlukan autentikasi JWT.**

    - **title**: Nama tugas (wajib)
    - **description**: Deskripsi tugas
    - **status**: Status tugas (pending / in_progress / done)
    - **event_id**: ID event yang terkait (wajib, harus valid)
    - **assigned_to**: ID user yang ditugaskan (opsional)
    """
    # Validasi: pastikan event_id ada
    db_event = get_event(db, task_data.event_id)
    if not db_event:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Event with id {task_data.event_id} not found. Cannot create task for non-existent event."
        )

    # Validasi status
    valid_statuses = ["pending", "in_progress", "done"]
    if task_data.status and task_data.status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status '{task_data.status}'. Must be one of: {valid_statuses}"
        )

    return create_task(db, task_data)


@router.get(
    "/",
    response_model=List[TaskResponse],
    summary="Lihat Semua Task"
)
def read_tasks(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Ambil daftar semua task dari seluruh event.
    Mendukung pagination dengan parameter `skip` dan `limit`.
    """
    return get_tasks(db, skip=skip, limit=limit)


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Detail Task"
)
def read_task(task_id: int, db: Session = Depends(get_db)):
    """
    Ambil detail satu task berdasarkan ID.
    """
    db_task = get_task(db, task_id)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return db_task


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Update Task"
)
def update_existing_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update data task. **Memerlukan autentikasi JWT.**

    Semua field bersifat opsional — hanya field yang dikirim yang akan diupdate.
    """
    db_task = get_task(db, task_id)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )

    # Validasi status jika dikirim
    valid_statuses = ["pending", "in_progress", "done"]
    if task_data.status and task_data.status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status '{task_data.status}'. Must be one of: {valid_statuses}"
        )

    updated = update_task(db, task_id, task_data)
    return updated


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_200_OK,
    summary="Hapus Task"
)
def delete_existing_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Hapus task berdasarkan ID. **Memerlukan autentikasi JWT.**
    """
    db_task = get_task(db, task_id)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )

    delete_task(db, task_id)
    return {"message": f"Task '{db_task.title}' has been deleted successfully"}


# ============================================================
# Endpoint tambahan: Task berdasarkan Event
# ============================================================
@router.get(
    "/by-event/{event_id}",
    response_model=List[TaskResponse],
    summary="Task Berdasarkan Event"
)
def read_tasks_by_event(event_id: int, db: Session = Depends(get_db)):
    """
    Ambil semua task yang terkait dengan event tertentu.
    """
    # Validasi: pastikan event ada
    db_event = get_event(db, event_id)
    if not db_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id {event_id} not found"
        )

    return get_tasks_by_event(db, event_id)

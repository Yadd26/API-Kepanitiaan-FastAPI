from sqlalchemy.orm import Session

from models.task import Task
from schemas.task import TaskCreate, TaskUpdate


def create_task(db: Session, task_data: TaskCreate):
    """Buat task baru."""
    db_task = Task(
        title=task_data.title,
        description=task_data.description,
        status=task_data.status or "pending",
        event_id=task_data.event_id,
        assigned_to=task_data.assigned_to
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    """Ambil semua task dengan pagination."""
    return db.query(Task).offset(skip).limit(limit).all()


def get_tasks_by_event(db: Session, event_id: int):
    """Ambil semua task berdasarkan event_id."""
    return db.query(Task).filter(Task.event_id == event_id).all()


def get_task(db: Session, task_id: int):
    """Ambil detail satu task berdasarkan ID."""
    return db.query(Task).filter(Task.id == task_id).first()


def update_task(db: Session, task_id: int, task_data: TaskUpdate):
    """Update task yang sudah ada."""
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        return None

    update_data = task_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)

    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int):
    """Hapus task berdasarkan ID. Mengembalikan True jika berhasil."""
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        return False
    db.delete(db_task)
    db.commit()
    return True

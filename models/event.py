from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(200), index=True, nullable=False)
    description = Column(Text, nullable=True)
    location = Column(String(200), nullable=True)
    event_date = Column(DateTime(timezone=True), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    # Relasi One-to-Many: Event memiliki banyak Task
    tasks = relationship("Task", back_populates="event", cascade="all, delete-orphan")
    # Relasi Many-to-One: Event dibuat oleh satu User
    creator = relationship("User", back_populates="events")

    def __repr__(self):
        return f"<Event(id={self.id}, title='{self.title}')>"

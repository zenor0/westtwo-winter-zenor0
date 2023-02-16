from typing import Optional
from sqlalchemy import String, create_engine, TIMESTAMP, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

class TodoTable(Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[Optional[str]] = mapped_column(String(256))
    content: Mapped[Optional[str]] = mapped_column(String(1024))
    status: Mapped[str] = mapped_column(String(45))
    add_time: Mapped[str] = mapped_column(TIMESTAMP)
    end_time: Mapped[str] = mapped_column(TIMESTAMP)

    def __repr__(self) -> dict:
        return {'id': self.id, 'title': self.title, 'content': self.content, 'status': self.status, 'add_time': self.add_time, 'end_time': self.end_time}
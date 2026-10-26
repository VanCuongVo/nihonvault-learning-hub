from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import String, Integer, DateTime, Enum as SQLEnum, Text, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.enums.JLPTLevel import JLPTLevel

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.example_sentence import ExampleSentence
    from app.models.user_bookmark import UserBookmark


class Kanji(Base):
    __tablename__ = "kanjis"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    character: Mapped[str] = mapped_column(String(10), unique=True, index=True, nullable=False)
    han_viet: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    onyomi: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    kunyomi: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    meaning_vi: Mapped[str] = mapped_column(Text, nullable=False)
    stroke_count: Mapped[int] = mapped_column(Integer, nullable=False)
    radical: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    
    jlpt_level: Mapped[JLPTLevel] = mapped_column(
        SQLEnum(JLPTLevel, name="jlpt_level_enum", native_enum=False),
        index=True,
        nullable=False
    )

    # Khóa ngoại liên kết người tạo (User)
    created_by_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Quan hệ
    creator: Mapped[Optional["User"]] = relationship(back_populates="created_kanjis")
    examples: Mapped[List["ExampleSentence"]] = relationship(
        back_populates="kanji", cascade="all, delete-orphan"
    )
    bookmarks: Mapped[List["UserBookmark"]] = relationship(
        back_populates="kanji", cascade="all, delete-orphan"
    )
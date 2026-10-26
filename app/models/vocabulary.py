from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import String, DateTime, Enum as SQLEnum, Text, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.enums.JLPTLevel import JLPTLevel
from app.enums.PartOfSpeech import PartOfSpeech

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.example_sentence import ExampleSentence
    from app.models.user_bookmark import UserBookmark


class Vocabulary(Base):
    __tablename__ = "vocabularies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    word: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    reading: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    romaji: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    han_viet: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    meaning_vi: Mapped[str] = mapped_column(Text, nullable=False)
    
    part_of_speech: Mapped[PartOfSpeech] = mapped_column(
        SQLEnum(PartOfSpeech, name="part_of_speech_enum", native_enum=False),
        nullable=False
    )
    
    jlpt_level: Mapped[JLPTLevel] = mapped_column(
        SQLEnum(JLPTLevel, name="jlpt_level_enum", native_enum=False),
        index=True,
        nullable=False
    )
    
    audio_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

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
    creator: Mapped[Optional["User"]] = relationship(back_populates="created_vocabularies")
    examples: Mapped[List["ExampleSentence"]] = relationship(
        back_populates="vocabulary", cascade="all, delete-orphan"
    )
    bookmarks: Mapped[List["UserBookmark"]] = relationship(
        back_populates="vocabulary", cascade="all, delete-orphan"
    )
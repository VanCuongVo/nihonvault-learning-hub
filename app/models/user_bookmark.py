from datetime import datetime
from typing import TYPE_CHECKING, Optional
from sqlalchemy import Text, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.kanji import Kanji
    from app.models.vocabulary import Vocabulary
    from app.models.grammar import Grammar


class UserBookmark(Base):
    __tablename__ = "user_bookmarks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # Liên kết với mục được lưu (chọn 1 trong 3)
    kanji_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("kanjis.id", ondelete="CASCADE"), nullable=True, index=True
    )
    vocab_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("vocabularies.id", ondelete="CASCADE"), nullable=True, index=True
    )
    grammar_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("grammars.id", ondelete="CASCADE"), nullable=True, index=True
    )

    note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # Ghi chú cá nhân của người học

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Quan hệ ngược về
    user: Mapped["User"] = relationship(back_populates="bookmarks")
    kanji: Mapped[Optional["Kanji"]] = relationship(back_populates="bookmarks")
    vocabulary: Mapped[Optional["Vocabulary"]] = relationship(back_populates="bookmarks")
    grammar: Mapped[Optional["Grammar"]] = relationship(back_populates="bookmarks")
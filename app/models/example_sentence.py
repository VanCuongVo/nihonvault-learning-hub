from datetime import datetime
from typing import TYPE_CHECKING, Optional
from sqlalchemy import String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.kanji import Kanji
    from app.models.vocabulary import Vocabulary
    from app.models.grammar import Grammar


class ExampleSentence(Base):
    __tablename__ = "example_sentences"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sentence_jp: Mapped[str] = mapped_column(Text, nullable=False)                 # Câu tiếng Nhật
    furigana: Mapped[Optional[str]] = mapped_column(Text, nullable=True)           # Phiên âm furigana hoặc romaji
    meaning_vi: Mapped[str] = mapped_column(Text, nullable=False)                  # Nghĩa tiếng Việt
    audio_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)  # File ghi âm câu mẫu

    # Khóa ngoại liên kết linh hoạt (nullable=True vì câu có thể minh họa cho từ vựng, ngữ pháp hoặc kanji)
    kanji_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("kanjis.id", ondelete="CASCADE"), nullable=True, index=True
    )
    vocab_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("vocabularies.id", ondelete="CASCADE"), nullable=True, index=True
    )
    grammar_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("grammars.id", ondelete="CASCADE"), nullable=True, index=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Quan hệ ngược về từng thực thể
    kanji: Mapped[Optional["Kanji"]] = relationship(back_populates="examples")
    vocabulary: Mapped[Optional["Vocabulary"]] = relationship(back_populates="examples")
    grammar: Mapped[Optional["Grammar"]] = relationship(back_populates="examples")
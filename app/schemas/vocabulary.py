from datetime import datetime
from pydantic import BaseModel, Field
from app.enums.JLPTLevel import JLPTLevel
from app.enums.PartOfSpeech import PartOfSpeech




# 4. Schema phân trang khi lấy danh sách
class PaginatedVocabularyResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: list[VocabularyResponse]


# 3. Schema hiển thị chi tiết từ vựng
class VocabularyResponse(BaseModel):
    id: int
    word: str
    reading: str
    meaning_vi: str
    part_of_speech: PartOfSpeech
    jlpt_level: JLPTLevel
    romaji: str | None
    han_viet: str | None
    audio_url: str | None
    created_by_id: int | None
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}



class VocabularyUpdateRequest(BaseModel):
    word: str | None = Field(default=None, max_length=100)
    reading: str | None = Field(default=None, max_length=100)
    meaning_vi: str | None = None
    part_of_speech: PartOfSpeech | None = None
    jlpt_level: JLPTLevel | None = None
    romaji: str | None = None
    han_viet: str | None = None
    audio_url: str | None = None



class VocabularyCreateRequest(BaseModel):
    word: str = Field(min_length=1, max_length=100, example="食べる")
    reading: str = Field(min_length=1, max_length=100, example="たべる")
    meaning_vi: str = Field(min_length=1, example="Ăn")
    part_of_speech: PartOfSpeech = Field(example=PartOfSpeech.VERB_GROUP_2)
    jlpt_level: JLPTLevel = Field(example=JLPTLevel.N5)
    romaji: str | None = Field(default=None, example="taberu")
    han_viet: str | None = Field(default=None, example="THỰC")
    audio_url: str | None = None


# Dữ liệu từng dòng đọc từ CSV
class VocabularyImportRow(BaseModel):
    word: str = Field(min_length=1, max_length=100)
    reading: str = Field(min_length=1, max_length=100)
    meaning_vi: str = Field(min_length=1)
    part_of_speech: PartOfSpeech
    jlpt_level: JLPTLevel
    romaji: str | None = None
    han_viet: str | None = None
    audio_url: str | None = None


# Trả về thông tin từ vựng
class VocabularyResponse(BaseModel):
    id: int
    word: str
    reading: str
    meaning_vi: str
    part_of_speech: PartOfSpeech
    jlpt_level: JLPTLevel
    han_viet: str | None
    created_by_id: int | None
    created_at: datetime

    model_config = {"from_attributes": True}


# Kết quả trả về sau khi import file
class VocabularyImportResult(BaseModel):
    total_rows: int
    success_count: int
    failed_count: int
    errors: list[dict] = []  # Lưu: [{"row": 5, "word": "食べる", "error": "Từ đã tồn tại"}]
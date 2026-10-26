from fastapi import APIRouter, Depends, Query, UploadFile, File, HTTPException, status
from dependencies import get_current_user
from app.services.vocabulary_service import VocabularyService
from app.repositories.unit_of_work import UnitOfWork
from app.enums.JLPTLevel import JLPTLevel
from app.enums.PartOfSpeech import PartOfSpeech
from app.schemas.api_response import APIResponse
from app.schemas.vocabulary import (
    VocabularyCreateRequest,
    VocabularyUpdateRequest,
    VocabularyResponse,
    PaginatedVocabularyResponse,
    VocabularyImportResult,
)

router = APIRouter(
    prefix="/vocabularies",
    tags=["Vocabularies"],
    dependencies=[Depends(get_current_user)]  # Khóa bảo mật: Cần đăng nhập
)

def get_vocab_service() -> VocabularyService:
    return VocabularyService(uow_factory=UnitOfWork)


# 1. LẤY DANH SÁCH (Phân trang + Tìm kiếm + Lọc)
@router.get("", response_model=APIResponse[PaginatedVocabularyResponse])
async def get_vocabularies(
    page: int = Query(default=1, ge=1, description="Số trang"),
    page_size: int = Query(default=20, ge=1, le=100, description="Số lượng mỗi trang"),
    search: str | None = Query(default=None, description="Tìm theo từ, cách đọc hoặc nghĩa"),
    jlpt_level: JLPTLevel | None = Query(default=None, description="Lọc theo cấp độ N5-N1"),
    part_of_speech: PartOfSpeech | None = Query(default=None, description="Lọc theo từ loại"),
    service: VocabularyService = Depends(get_vocab_service),
):
    result = await service.get_all(
        page=page,
        page_size=page_size,
        search=search,
        jlpt_level=jlpt_level,
        part_of_speech=part_of_speech,
    )
    return APIResponse(success=True, message="Lấy danh sách thành công", data=result)


# 2. XEM CHI TIẾT THEO ID
@router.get("/{vocab_id}", response_model=APIResponse[VocabularyResponse])
async def get_vocabulary(
    vocab_id: int,
    service: VocabularyService = Depends(get_vocab_service)
):
    try:
        result = await service.get_by_id(vocab_id)
        return APIResponse(success=True, message="Lấy chi tiết thành công", data=result)
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


# 3. TẠO 1 TỪ VỰNG MỚI
@router.post("", response_model=APIResponse[VocabularyResponse], status_code=status.HTTP_201_CREATED)
async def create_vocabulary(
    request: VocabularyCreateRequest,
    current_user: dict = Depends(get_current_user),
    service: VocabularyService = Depends(get_vocab_service),
):
    try:
        result = await service.create(request, user_id=current_user["id"])
        return APIResponse(success=True, message="Tạo từ vựng thành công", data=result)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))


# 4. CHỈNH SỬA TỪ VỰNG
@router.put("/{vocab_id}", response_model=APIResponse[VocabularyResponse])
async def update_vocabulary(
    vocab_id: int,
    request: VocabularyUpdateRequest,
    service: VocabularyService = Depends(get_vocab_service),
):
    try:
        result = await service.update(vocab_id, request)
        return APIResponse(success=True, message="Cập nhật từ vựng thành công", data=result)
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


# 5. XÓA TỪ VỰNG
@router.delete("/{vocab_id}", response_model=APIResponse[None])
async def delete_vocabulary(
    vocab_id: int,
    service: VocabularyService = Depends(get_vocab_service)
):
    try:
        await service.delete(vocab_id)
        return APIResponse(success=True, message="Đã xóa từ vựng thành công", data=None)
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


# 6. IMPORT FILE (CSV / EXCEL)
@router.post("/import-file", response_model=APIResponse[VocabularyImportResult])
async def import_vocabularies(
    file: UploadFile = File(..., description="File Excel .xlsx hoặc CSV"),
    current_user: dict = Depends(get_current_user),
    service: VocabularyService = Depends(get_vocab_service),
):
    try:
        result = await service.import_from_file(file, user_id=current_user["id"])
        return APIResponse(
            success=True,
            message=f"Đã import thành công {result.success_count}/{result.total_rows} từ vựng",
            data=result,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
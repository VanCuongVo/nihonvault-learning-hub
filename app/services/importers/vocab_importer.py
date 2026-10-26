import csv
import io
from fastapi import UploadFile
from pydantic import ValidationError
from app.schemas.vocabulary import VocabularyImportRow


class VocabCSVImporter:

    @staticmethod
    async def parse_csv(file: UploadFile) -> tuple[list[VocabularyImportRow], list[dict]]:
        """
        Đọc nội dung CSV, trả về:
        - valid_rows: danh sách các dòng hợp lệ (đã pass Pydantic)
        - errors: danh sách các dòng lỗi cấu trúc/dữ liệu
        """
        content = await file.read()
        
        # utf-8-sig giúp giải mã chuẩn các ký tự tiếng Nhật và xóa ký tự BOM nếu có
        try:
            text_data = content.decode("utf-8-sig")
        except UnicodeDecodeError:
            raise ValueError("File phải được mã hóa theo chuẩn UTF-8 hoặc UTF-8 with BOM")

        reader = csv.DictReader(io.StringIO(text_data))
        valid_rows: list[VocabularyImportRow] = []
        errors: list[dict] = []

        for index, row in enumerate(reader, start=2):  # Dòng 1 là Header, bắt đầu đọc từ dòng 2
            # Bỏ khoảng trắng dư thừa ở các giá trị
            cleaned_row = {k.strip(): v.strip() for k, v in row.items() if k and v}
            
            try:
                item = VocabularyImportRow(**cleaned_row)
                valid_rows.append(item)
            except ValidationError as e:
                error_msg = "; ".join([f"{err['loc'][0]}: {err['msg']}" for err in e.errors()])
                errors.append({
                    "row": index,
                    "word": cleaned_row.get("word", "N/A"),
                    "error": error_msg
                })

        return valid_rows, errors
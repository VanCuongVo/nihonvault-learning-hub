from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.config import settings
from app.core.database import engine
from dependencies import get_db
from app.routes.auth_routes import router as auth_router  
from app.routes.vocabulary_routes import router as vocab_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Khởi động app: kiểm tra kết nối DB sơ bộ
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        print("Kết nối PostgreSQL thành công!")
    except Exception as e:
        print(f"Không thể kết nối PostgreSQL: {e}")
    yield
    # Dọn dẹp tài nguyên khi tắt server
    await engine.dispose()
    print("Đã giải phóng toàn bộ DB pool.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)

app.include_router(auth_router)
app.include_router(vocab_router)

@app.get("/")
async def root():
    return {"message": f"Chào mừng bạn đến với {settings.PROJECT_NAME} API!"}

@app.get("/health/db")
async def check_db_health(db: AsyncSession = Depends(get_db)):
    """Kiểm tra trạng thái kết nối tới PostgreSQL từ Request Session."""
    try:
        result = await db.execute(text("SELECT 1"))
        scalar_val = result.scalar()
        return {
            "database": "PostgreSQL",
            "status": "connected",
            "check": scalar_val == 1
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection error: {str(e)}"
        )

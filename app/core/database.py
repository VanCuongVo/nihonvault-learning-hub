from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

# 1. Khởi tạo Async Engine kết nối PostgreSQL
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,                    # Log SQL query ra console khi DEBUG=True
    pool_size=settings.DB_POOL_SIZE,        # Số connection tối đa giữ cố định trong Pool
    max_overflow=settings.DB_MAX_OVERFLOW,  # Số connection cho phép mở tạm thêm khi tải cao
    pool_pre_ping=True,                     # Kiểm tra kết nối còn sống trước khi cấp cho session
    pool_recycle=1800,                      # Tự động refresh kết nối sau 30 phút
)

# 2. Tạo Session Factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,                 # Cho phép truy cập thuộc tính object sau khi commit
)

# 3. Base class cho toàn bộ ORM Models kế thừa
class Base(DeclarativeBase):
    pass

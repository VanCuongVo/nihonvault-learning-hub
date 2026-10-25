import bcrypt

class PasswordHasher:
    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        # BCrypt nhận dữ liệu dạng bytes, trong khi mật khẩu thông thường là chuỗi str.
        # password.encode("utf-8") : bytes
        # decode("utf-8") : chuyển thành chuỗi để lưu
        return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    
    
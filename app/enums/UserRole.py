from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    GUEST = "Guest"
    STUDENT = "student"

from pydantic import BaseModel,EmailStr
from enum import Enum

class LoginSchema(BaseModel):
    username: str
    password: str

class UserRole(str, Enum):
    admin = "admin"
    customer = "customer"

class SignupSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    confirm_password: str
    role: UserRole
# pydantic models will be created here
from pydantic import BaseModel


class UserBase(BaseModel):
    email: str = None


class UserCreate(BaseModel):
    email: str = None
    password: str = None
    confirm_password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "sample@gmail.com",
                "password": "a_difficult_password",
                "confirm_password": "a_difficult_password"
            }
        }


class UserLogin(BaseModel):
    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "sample@gmail.com",
                "password": "a_difficult_password"
            }
        }


class UserModel(UserBase):
    id: int

    class Config:
        orm_mode = True

# schemas for category


class CategoryBase(BaseModel):
    name: str = None


class CategoryCreate(CategoryBase):
    pass


class CategoryModel(CategoryBase):
    id: int

    class Config:
        orm_mode = True

# schemas for blog


class BlogBase(BaseModel):
    title: str
    content: str
    author: int
    category: int


class BlogCreate(BlogBase):
    pass


class BlogModel(BlogBase):
    id: int

    class Config:
        orm_mode = True

# 18e0fe2dadf7aedcd03f485ad1cc91d271ed33e7e25847cce3881869318f6e9f

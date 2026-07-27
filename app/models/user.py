from pydantic import BaseModel, Field
from typing import Optional

class UserBase(BaseModel):
    username: str = Field(..., example="operador_ot")
    email: Optional[str] = Field(None, example="operador@planta.com")

class UserCreate(UserBase):
    password: str = Field(..., example="PasswordSeguro123!")

class UserResponse(UserBase):
    id: int
    is_active: bool = True

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

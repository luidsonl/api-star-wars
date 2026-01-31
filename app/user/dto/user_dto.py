from pydantic import BaseModel, EmailStr, Field

class UserCreateDTO(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    name: str

class UserResponseDTO(BaseModel):
    id: str
    email: EmailStr
    name: str

class UserLoginDTO(BaseModel):
    email: EmailStr
    password: str

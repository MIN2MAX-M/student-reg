from pydantic import BaseModel, EmailStr, Field


class StudentBase(BaseModel):
    first_name: str = Field(min_length=1, max_length=80)
    last_name: str = Field(min_length=1, max_length=80)
    email: EmailStr
    phone: str | None = Field(default=None, max_length=32)
    age: int | None = Field(default=None, ge=0, le=130)
    address: str | None = Field(default=None, max_length=255)


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    first_name: str | None = Field(default=None, min_length=1, max_length=80)
    last_name: str | None = Field(default=None, min_length=1, max_length=80)
    phone: str | None = Field(default=None, max_length=32)
    age: int | None = Field(default=None, ge=0, le=130)
    address: str | None = Field(default=None, max_length=255)


class StudentOut(StudentBase):
    id: int

    class Config:
        from_attributes = True

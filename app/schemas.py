from pydantic import BaseModel,Field
from typing import Optional

# ---------- USERS ----------
class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str = Field(min_length=1, max_length=72)  
    role: str = "user"  

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None

class UserOut(UserBase):
    id: int
    role: str

    class Config:
        from_attributes = True


# ---------- ORDERS ----------
class OrderBase(BaseModel):
    total_amount: int = 0
    status: str = "created"

class OrderCreate(OrderBase):
    # user_id optional: normal users create for themselves; admin can create for anyone
    user_id: Optional[int] = None

class OrderUpdate(BaseModel):
    total_amount: Optional[int] = None
    status: Optional[str] = None

class OrderOut(OrderBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
       
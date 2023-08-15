from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
  first_name: str
  last_name: str
  email_address: str

  
class UserCreate(UserBase):
    password: str
    

class User(UserBase):
    id: int
    
    class Config:
        from_attributes = True
        
class GetUser(BaseModel):
    user_id: int
    
class GetUsers(BaseModel):
    offset: Optional[int] = 0
    limit: Optional[int] = 10
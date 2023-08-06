import uuid
from typing import List, Optional
import pydantic
from pydantic import BaseModel
import json
from enum import Enum
from datetime import datetime


class AppUsers(BaseModel):
    uid: uuid.UUID
    username: str
    phone: str
    email: str
    password: str
    user_type: str
    is_locked:str
    is_verified: str
    is_deleted: str
    created_date: datetime
    class Config:
            orm_mode = True
            
    def __hash__(self):
        return hash(str(self.uid))

    def __eq__(self,other):
        return self.uid == other.uid
    

class AppUserVerification(BaseModel):
    uid: uuid.UUID
    user_uid:uuid.UUID
    verification_code:str
    class Config:
            orm_mode = True
            
    def __hash__(self):
        return hash(str(self.uid))

    def __eq__(self,other):
        return self.uid == other.uid

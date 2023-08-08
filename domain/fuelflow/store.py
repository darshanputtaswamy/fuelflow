import uuid
from typing import List, Optional
import pydantic
from pydantic import BaseModel
import json
from enum import Enum
from datetime import datetime
from domain.core.app_users import AppUsers


class Store(BaseModel):
    uid: uuid.UUID
    buisness_name: str
    type: str
    address: str
    postal_code: str
    gst_number: str
    is_deleted: str
    created_date: datetime
    updated_date: Optional[datetime]
    class Config:
            orm_mode = True
            
    def __hash__(self):
        return hash(str(self.uid))

    def __eq__(self,other):
        return self.uid == other.uid
    
class StoreUserPrivilege(BaseModel):
    uid: uuid.UUID
    user_uid:uuid.UUID
    store_uid:uuid.UUID
    role:str
    created_date:datetime
    updated_date:Optional[datetime]

    class Config:
            orm_mode = True
            
    def __hash__(self):
        return hash(str(self.uid))

    def __eq__(self,other):
        return self.uid == other.uid


class StoreActivities(BaseModel):
    uid: uuid.UUID
    store_uid:uuid.UUID
    activity_type:str
    class Config:
            orm_mode = True
            
    def __hash__(self):
        return hash(str(self.uid))

    def __eq__(self,other):
        return self.uid == other.uid
    

class StoreRoles(BaseModel):
    uid: uuid.UUID
    store_uid:uuid.UUID
    roles:str
    class Config:
            orm_mode = True
            
    def __hash__(self):
        return hash(str(self.uid))

    def __eq__(self,other):
        return self.uid == other.uid
    


class StoreRota(BaseModel):
    uid: uuid.UUID
    store_uid:uuid.UUID
    user_uid:uuid.UUID
    from_date: datetime
    till_date: datetime
    role_uid:uuid.UUID
    activity_uid:uuid.UUID
    approval_status:str

    class Config:
            orm_mode = True
            
    def __hash__(self):
        return hash(str(self.uid))

    def __eq__(self,other):
        return self.uid == other.uid
    

class POS(BaseModel):
    uid: uuid.UUID
    store_uid:uuid.UUID
    pos_name:str
    pos_type: str
    pos_contact_uid: uuid.UUID
    created_date:datetime
    updated_date:Optional[datetime]

    class Config:
            orm_mode = True
            
    def __hash__(self):
        return hash(str(self.uid))

    def __eq__(self,other):
        return self.uid == other.uid
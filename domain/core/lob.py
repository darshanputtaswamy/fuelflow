import uuid
from typing import List, Optional
import pydantic
from pydantic import BaseModel
import json
from enum import Enum
from datetime import datetime
from domain.core.app_users import AppUsers


class LOB(BaseModel):
    uid: uuid.UUID
    buisness_name: str
    type: str
    address: str
    postal_code: str
    gst_number: str
    subscription_status:str
    is_deleted: str
    created_date: datetime
    updated_date: Optional[datetime]
    class Config:
            orm_mode = True
            
    def __hash__(self):
        return hash(str(self.uid))

    def __eq__(self,other):
        return self.uid == other.uid
    
class LOBUserPrivilege(BaseModel):
    uid: uuid.UUID
    user_uid:uuid.UUID
    lob_uid:uuid.UUID
    role:str
    created_date:datetime
    updated_date:Optional[datetime]

    class Config:
            orm_mode = True
            
    def __hash__(self):
        return hash(str(self.uid))

    def __eq__(self,other):
        return self.uid == other.uid


class LOBActivities(BaseModel):
    uid: uuid.UUID
    lob_uid:uuid.UUID
    activity_type:str
    class Config:
            orm_mode = True
            
    def __hash__(self):
        return hash(str(self.uid))

    def __eq__(self,other):
        return self.uid == other.uid
    

class LOBRoles(BaseModel):
    uid: uuid.UUID
    lob_uid:uuid.UUID
    roles:str
    class Config:
            orm_mode = True
            
    def __hash__(self):
        return hash(str(self.uid))

    def __eq__(self,other):
        return self.uid == other.uid
    


class LOBRota(BaseModel):
    uid: uuid.UUID
    lob_uid:uuid.UUID
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
    lob_uid:uuid.UUID
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
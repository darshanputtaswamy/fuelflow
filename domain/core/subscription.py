import uuid
from typing import List, Optional
import pydantic
from pydantic import BaseModel
import json
from enum import Enum
from datetime import datetime
from domain.core.app_users import AppUsers
from domain.core.lob import LOB


class Plans(BaseModel):
    uid: uuid.UUID
    plan_type:str
    plan_name: str
    price: float
    period: int
    key: str
    retention_limit: int
    user_limit:int
    status: str
    created_date: datetime
    updated_date:Optional[datetime]
    class Config:
            orm_mode = True
            
    def __hash__(self):
        return hash(str(self.uid))

    def __eq__(self,other):
        return self.uid == other.uid
    

class SubscriptionOrders(BaseModel):
    uid: uuid.UUID
    lob_uid:uuid.UUID
    initiated_user_uid:uuid.UUID
    plan_id:uuid.UUID
    paid_amount:float
    receipt_id:str
    status:str
    payment_id:str
    order_id:str
    signature:str
    created_date:datetime
    updated_date:Optional[datetime]

    class Config:
            orm_mode = True
            
    def __hash__(self):
        return hash(str(self.uid))

    def __eq__(self,other):
        return self.uid == other.uid

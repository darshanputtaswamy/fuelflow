import uuid
from typing import List, Optional
import pydantic
from pydantic import BaseModel
import json
from enum import Enum
from datetime import datetime
from domain.core.app_users import AppUsers
from domain.fuel.lob import LOB

class PlanType(str):
    free = "free"
    basic = "basic"
    premium = "premium"

class SubscriptionStatus(str):
    active = "active"
    inactive = "inactive"
    pending = "pending"

class PlanStatus(str):
    active = "active"
    inactive = "inactive"


class Plans(BaseModel):
    uid: uuid.UUID
    plan_type:PlanType
    plan_name: str
    price: float
    period: int
    key: str
    retention_limit: int
    user_limit:int
    status: PlanStatus
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
    status:SubscriptionStatus
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

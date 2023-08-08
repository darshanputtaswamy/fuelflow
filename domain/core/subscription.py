import uuid
from typing import List, Optional
import pydantic
from pydantic import BaseModel
import json
from enum import Enum
from datetime import datetime
from domain.core.app_users import AppUsers
from domain.fuelflow.lob import LOB

class PlanType(str):
    free = "free"
    basic = "basic"
    premium = "premium"

class SubscriptionStatus(str):
    active = "active"
    inactive = "inactive"

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
    

class Subscription(BaseModel):
    uid: uuid.UUID
    lob_uid:uuid.UUID
    initiated_user_uid:uuid.UUID
    plan_id:uuid.UUID
    plan_start_date:Optional[datetime]
    status:SubscriptionStatus
    created_date:datetime
    updated_date:Optional[datetime]

    class Config:
            orm_mode = True
            
    def __hash__(self):
        return hash(str(self.uid))

    def __eq__(self,other):
        return self.uid == other.uid



class SubscriptionPaymentOrder(BaseModel):
    uid: uuid.UUID
    subscription_uid: uuid.UUID
    receipt_id:str
    payable_amount:float
    pyament_id:str
    order_id:str
    signature:str
    status:str
    created_at:datetime
    updated_at:Optional[datetime]
  

    class Config:
            orm_mode = True
            
    def __hash__(self):
        return hash(str(self.uid))

    def __eq__(self,other):
        return self.uid == other.uid

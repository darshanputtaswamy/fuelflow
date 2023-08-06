import uuid
from typing import List, Optional
import pydantic
from pydantic import BaseModel, Field
import json
from enum import Enum
from datetime import datetime
from domain.core.app_users import AppUsers
from domain.core.lob import LOB


class Vehicles(BaseModel):
    uid: uuid.UUID
    lob_uid:uuid.UUID
    user_uid: uuid.UUID
    vehicle_num:str
    status: str
   
    class Config:
            orm_mode = True
            
    def __hash__(self):
        return hash(str(self.uid))

    def __eq__(self,other):
        return self.uid == other.uid
    


class Orders(BaseModel):
    uid: uuid.UUID
    lob_uid:uuid.UUID
    pos_uid: uuid.UUID
    rota_uid: uuid.UUID
    user_uid:str
    total_amount: float
    type:str
    payment_mode:Optional[str]
    created_date:datetime
    updated_date:Optional[datetime]
    class Config:
            orm_mode = True
            
    def __hash__(self):
        return hash(str(self.uid))

    def __eq__(self,other):
        return self.uid == other.uid
    
class OrdersLineItem(BaseModel):
    uid: uuid.UUID
    order_id:uuid.UUID
    vehicle_id: uuid.UUID
    liters: float
    rate:float
    amount: float
    class Config:
            orm_mode = True
            
    def __hash__(self):
        return hash(str(self.uid))

    def __eq__(self,other):
        return self.uid == other.uid
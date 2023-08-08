import uuid
from typing import List, Optional
import pydantic
from pydantic import BaseModel, Field
import json
from enum import Enum
from datetime import datetime
from domain.core.app_users import AppUsers
from domain.fuelflow.store import Store




class FuelDipReader(BaseModel):
    uid: uuid.UUID
    store_uid:uuid.UUID
    fuel_tank: str
    dip_number: float
    liters:float
    class Config:
            orm_mode = True
            
    def __hash__(self):
        return hash(str(self.uid))

    def __eq__(self,other):
        return self.uid == other.uid
    
class FuelUnloadingBook(BaseModel):
    uid: uuid.UUID
    store_uid:uuid.UUID
    unload_date: datetime
    fuel_tank:str
    vehicle_number:str
    depo_name:str
    sample_box:str
    before_unload_dip_reading:Optional[float]
    before_unload_liters:Optional[float]
    after_unload_dip_reading:Optional[float]
    after_unload_liters:Optional[float]
    sales:Optional[float]
    bill_density:Optional[float]
    check_density:Optional[float]

    class Config:
            orm_mode = True
            
    def __hash__(self):
        return hash(str(self.uid))

    def __eq__(self,other):
        return self.uid == other.uid
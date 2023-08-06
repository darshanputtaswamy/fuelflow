import uuid
from typing import List, Optional
import pydantic
from pydantic import BaseModel, Field
import json
from enum import Enum
from datetime import datetime
from domain.core.app_users import AppUsers
from domain.fuel.lob import LOB


class Record(BaseModel):
    uid: uuid.UUID
    lob_uid:uuid.UUID
    pos_uid: uuid.UUID
    rota_uid: uuid.UUID
    previous_uid: Optional[str]
    status: str
    closing_reading:float
    opening_reading:float
    total_sales:float
    rate:float
    total:float
    cash_amount_received:float
    card_amount_received:float
    upi_amount_received:float
    credits:float
    expenditure:float
    balance:float
    class Config:
            orm_mode = True
            
    def __hash__(self):
        return hash(str(self.uid))

    def __eq__(self,other):
        return self.uid == other.uid

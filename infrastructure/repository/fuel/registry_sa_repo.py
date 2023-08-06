from infrastructure.repository.base import AbstractRepository
from infrastructure.persistence.orm.models import FuelRegistryORM
from domain.fuel.registry import Record
from sqlalchemy.orm import load_only


class FuelRegistrySQLAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, v):
        v_in_orm=FuelRegistryORM(**v.dict())
        self.session.add(v_in_orm)

    def getByReference(self, **reference):
        r_in_orm=self.session.query(FuelRegistryORM).filter_by(**reference)
        res=[]
        for sh in r_in_orm:
            res.append(Record.from_orm(sh))
        return res
    
    def get(self, id):
         v_in_orm=self.session.get(FuelRegistryORM,str(id))
         if v_in_orm is not None:
            return Record.from_orm(v_in_orm)
         else:
             return None

    def list(self):
        v_in_orm=self.session.query(FuelRegistryORM).all()
        res=[]
        for RCA in v_in_orm:
            res.append(Record.from_orm(RCA))
        return res
        

    def delete(self,id):
        v_in_orm=self.session.get(FuelRegistryORM,str(id))
        self.session.delete(v_in_orm)

    def update(self,user):
        tdict=user.dict()
        tdict['uid']=str(tdict['uid'])
        v_in_orm=self.session.get(FuelRegistryORM,tdict['uid'])
        v_in_orm.lob_uid=str(tdict['lob_uid'])
        v_in_orm.pos_uid=str(tdict['pos_uid'])
        v_in_orm.rota_uid=str(tdict['rota_uid'])
        v_in_orm.previous_uid=str(tdict['previous_uid'])
        v_in_orm.status=tdict['status']
        v_in_orm.closing_reading=tdict['closing_reading']
        v_in_orm.opening_reading=tdict['opening_reading']
        v_in_orm.total_sales=tdict['total_sales']
        v_in_orm.rate=tdict['rate']
        v_in_orm.total=tdict['total']
        v_in_orm.cash_amount_received=tdict['cash_amount_received']
        v_in_orm.card_amount_received=tdict['card_amount_received']
        v_in_orm.upi_amount_received=tdict['upi_amount_received']
        v_in_orm.credits=tdict['credits']
        v_in_orm.expenditure=tdict['expenditure']
        v_in_orm.balance=tdict['balance']

        self.session.add(v_in_orm)


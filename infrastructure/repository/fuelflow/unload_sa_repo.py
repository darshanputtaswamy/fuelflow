from infrastructure.repository.base import AbstractRepository
from infrastructure.persistence.orm.models import FuelDipReaderORM,FuelUnloadingBookORM
from domain.fuelflow.unloader import FuelDipReader,FuelUnloadingBook
from sqlalchemy.orm import load_only


class FuelDipReaderSQLAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, v):
        v_in_orm=FuelDipReaderORM(**v.dict())
        self.session.add(v_in_orm)

    def getByReference(self, **reference):
        v_in_orm=self.session.query(FuelDipReaderORM).filter_by(**reference)
        res=[]
        for sh in v_in_orm:
            res.append(FuelDipReader.from_orm(sh))
        return res
    
    def get(self, id):
         v_in_orm=self.session.get(FuelDipReaderORM,str(id))
         if v_in_orm is not None:
            return FuelDipReader.from_orm(v_in_orm)
         else:
             return None

    def list(self):
        v_in_orm=self.session.query(FuelDipReaderORM).all()
        res=[]
        for RCA in v_in_orm:
            res.append(FuelDipReader.from_orm(RCA))
        return res
        

    def delete(self,id):
        v_in_orm=self.session.get(FuelDipReaderORM,str(id))
        self.session.delete(v_in_orm)

    def update(self,user):
        tdict=user.dict()
        tdict['uid']=str(tdict['uid'])
        v_in_orm=self.session.get(FuelDipReaderORM,tdict['uid'])
        v_in_orm.lob_uid=str(tdict['lob_uid'])
        v_in_orm.fuel_tank=str(tdict['fuel_tank'])
        v_in_orm.dip_number=tdict['dip_number']
        v_in_orm.liters=tdict['liters']
        self.session.add(v_in_orm)



class UnloaderSQLAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, o):
        o_in_orm=FuelUnloadingBookORM(**o.dict())
        self.session.add(o_in_orm)

    def getByReference(self, **reference):
        o_in_orm=self.session.query(FuelUnloadingBookORM).filter_by(**reference)
        res=[]
        for sh in o_in_orm:
            res.append(FuelUnloadingBook.from_orm(sh))
        return res
    
    def get(self, id):
         o_in_orm=self.session.get(FuelUnloadingBookORM,str(id))
         if o_in_orm is not None:
            return FuelUnloadingBook.from_orm(o_in_orm)
         else:
             return None

    def list(self):
        o_in_orm=self.session.query(FuelUnloadingBookORM).all()
        res=[]
        for RCA in o_in_orm:
            res.append(FuelUnloadingBook.from_orm(RCA))
        return res
        

    def delete(self,id):
        o_in_orm=self.session.get(FuelUnloadingBookORM,str(id))
        self.session.delete(o_in_orm)

    def update(self,user):
        tdict=user.dict()
        tdict['uid']=str(tdict['uid'])
        o_in_orm=self.session.get(FuelUnloadingBookORM,tdict['uid'])
        o_in_orm.lob_uid=str(tdict['lob_uid'])
        o_in_orm.unload_date=tdict['unload_date']
        o_in_orm.fuel_tank=tdict['fuel_tank']
        o_in_orm.vehicle_number=tdict['vehicle_number']
        o_in_orm.depo_name=tdict['depo_name']
        o_in_orm.sample_box=tdict['sample_box']
        o_in_orm.before_unload_dip_reading=tdict['before_unload_dip_reading']
        o_in_orm.before_unload_liters=tdict['before_unload_liters']
        o_in_orm.after_unload_dip_reading=tdict['after_unload_dip_reading']
        o_in_orm.after_unload_liters=tdict['after_unload_liters']
        o_in_orm.sales=tdict['sales']
        o_in_orm.bill_density=tdict['bill_density']
        o_in_orm.check_density=tdict['check_density']
        self.session.add(o_in_orm)


from infrastructure.repository.base import AbstractRepository
from infrastructure.persistence.orm.models import StoreCreditVehiclesORM,StoreCreditOrdersORM,StoreCreditOrderLineItemsORM
from domain.fuelflow.credit import Vehicles, Orders, OrdersLineItem
from sqlalchemy.orm import load_only


class VechiclesSQLAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, v):
        v_in_orm=StoreCreditVehiclesORM(**v.dict())
        self.session.add(v_in_orm)

    def getByReference(self, **reference):
        v_in_orm=self.session.query(StoreCreditVehiclesORM).filter_by(**reference)
        res=[]
        for sh in v_in_orm:
            res.append(Vehicles.from_orm(sh))
        return res
    
    def get(self, id):
         v_in_orm=self.session.get(StoreCreditVehiclesORM,str(id))
         if v_in_orm is not None:
            return Vehicles.from_orm(v_in_orm)
         else:
             return None

    def list(self):
        v_in_orm=self.session.query(StoreCreditVehiclesORM).all()
        res=[]
        for RCA in v_in_orm:
            res.append(Vehicles.from_orm(RCA))
        return res
        

    def delete(self,id):
        v_in_orm=self.session.get(StoreCreditVehiclesORM,str(id))
        self.session.delete(v_in_orm)

    def update(self,user):
        tdict=user.dict()
        tdict['uid']=str(tdict['uid'])
        v_in_orm=self.session.get(StoreCreditVehiclesORM,tdict['uid'])
        v_in_orm.store_uid=str(tdict['store_uid'])
        v_in_orm.user_uid=str(tdict['user_uid'])
        v_in_orm.vehicle_num=tdict['vehicle_num']
        v_in_orm.status=tdict['status']
        self.session.add(v_in_orm)


class OrderSQLAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, o):
        o_in_orm=StoreCreditOrdersORM(**o.dict())
        self.session.add(o_in_orm)

    def getByReference(self, **reference):
        o_in_orm=self.session.query(StoreCreditOrdersORM).filter_by(**reference)
        res=[]
        for sh in o_in_orm:
            res.append(Orders.from_orm(sh))
        return res
    
    def get(self, id):
         o_in_orm=self.session.get(StoreCreditOrdersORM,str(id))
         if o_in_orm is not None:
            return Orders.from_orm(o_in_orm)
         else:
             return None

    def list(self):
        o_in_orm=self.session.query(StoreCreditOrdersORM).all()
        res=[]
        for RCA in o_in_orm:
            res.append(Orders.from_orm(RCA))
        return res
        

    def delete(self,id):
        o_in_orm=self.session.get(StoreCreditOrdersORM,str(id))
        self.session.delete(o_in_orm)

    def update(self,user):
        tdict=user.dict()
        tdict['uid']=str(tdict['uid'])
        o_in_orm=self.session.get(StoreCreditOrdersORM,tdict['uid'])
        o_in_orm.store_uid=str(tdict['store_uid'])
        o_in_orm.pos_uid=str(tdict['pos_uid'])
        o_in_orm.rota_uid=str(tdict['rota_uid'])
        o_in_orm.user_uid=str(tdict['user_uid'])
        o_in_orm.total_amount=tdict['total_amount']
        o_in_orm.type=tdict['type']
        o_in_orm.payment_mode=tdict['payment_mode']
        o_in_orm.updated_date=tdict['updated_date']
        self.session.add(o_in_orm)




class OrderLineItemSQLAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, ol):
        ol_in_orm=StoreCreditOrderLineItemsORM(**ol.dict())
        self.session.add(ol_in_orm)

    def getByReference(self, **reference):
        ol_in_orm=self.session.query(StoreCreditOrderLineItemsORM).filter_by(**reference)
        res=[]
        for sh in ol_in_orm:
            res.append(OrdersLineItem.from_orm(sh))
        return res
    
    def get(self, id):
         ol_in_orm=self.session.get(StoreCreditOrderLineItemsORM,str(id))
         if ol_in_orm is not None:
            return OrdersLineItem.from_orm(ol_in_orm)
         else:
             return None

    def list(self):
        ol_in_orm=self.session.query(StoreCreditOrderLineItemsORM).all()
        res=[]
        for RCA in ol_in_orm:
            res.append(OrdersLineItem.from_orm(RCA))
        return res
        

    def delete(self,id):
        ol_in_orm=self.session.get(StoreCreditOrderLineItemsORM,str(id))
        self.session.delete(ol_in_orm)

    def update(self,user):
        tdict=user.dict()
        tdict['uid']=str(tdict['uid'])
        ol_in_orm=self.session.get(StoreCreditOrderLineItemsORM,tdict['uid'])
        ol_in_orm.order_id=str(tdict['order_id'])
        ol_in_orm.vehicle_id=str(tdict['vehicle_id'])
        ol_in_orm.liters=tdict['liters']
        ol_in_orm.rate=tdict['rate']
        ol_in_orm.amount=tdict['amount']
        self.session.add(ol_in_orm)

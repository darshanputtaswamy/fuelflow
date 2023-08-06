from infrastructure.repository.base import AbstractRepository
from infrastructure.persistence.orm.models import PlansORM,SubscriptionOrdersORM
from domain.core.subscription import Plans, SubscriptionOrders
from sqlalchemy.orm import load_only


class PlansSQLAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, plan):
        plan_in_orm=PlansORM(**plan.dict())
        self.session.add(plan_in_orm)

    def getByReference(self, **reference):
        sh_in_orm=self.session.query(PlansORM).filter_by(**reference)
        res=[]
        for sh in sh_in_orm:
            res.append(Plans.from_orm(sh))
        return res
    
    def get(self, id):
         plan_in_orm=self.session.get(PlansORM,str(id))
         if plan_in_orm is not None:
            return Plans.from_orm(plan_in_orm)
         else:
             return None

    def list(self):
        plan_in_orm=self.session.query(PlansORM).all()
        res=[]
        for RCA in plan_in_orm:
            res.append(Plans.from_orm(RCA))
        return res
        

    def delete(self,id):
        plan_in_orm=self.session.get(PlansORM,str(id))
        self.session.delete(plan_in_orm)

    def update(self,user):
        tdict=user.dict()
        tdict['uid']=str(tdict['uid'])
        plan_in_orm=self.session.get(PlansORM,tdict['uid'])
        plan_in_orm.plan_type = tdict['plan_type']
        plan_in_orm.plan_name = tdict['plan_name']
        plan_in_orm.price =tdict['price']
        plan_in_orm.period = tdict['period']
        plan_in_orm.key = tdict['key']
        plan_in_orm.retention_limit = tdict['retention_limit']
        plan_in_orm.user_limit=tdict['user_limit']
        plan_in_orm.status=tdict['status']
        plan_in_orm.updated_date=tdict['updated_date']
        self.session.add(plan_in_orm)




class SubscriptionOrdersSQLAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, sub):
        sub_in_orm=SubscriptionOrdersORM(**sub.dict())
        self.session.add(sub_in_orm)
    
    def get(self, id):
         sub_in_orm=self.session.get(SubscriptionOrdersORM,str(id))
         if sub_in_orm is not None:
            return SubscriptionOrders.from_orm(sub_in_orm)
         else:
             return None

    def list(self):
        sub_in_orm=self.session.query(SubscriptionOrdersORM).all()
        res=[]
        for s in sub_in_orm:
            res.append(SubscriptionOrders.from_orm(s))
        return res

    def getByReference(self, **reference):
        sh_in_orm=self.session.query(SubscriptionOrdersORM).filter_by(**reference)
        res=[]
        for sh in sh_in_orm:
            res.append(SubscriptionOrders.from_orm(sh))
        return res
    

    def delete(self,id):
        sub_in_orm=self.session.get(SubscriptionOrdersORM,str(id))
        self.session.delete(sub_in_orm)


    def update(self,user):
        tdict=user.dict()
        tdict['uid']=str(tdict['uid'])
        sub_in_orm=self.session.get(SubscriptionOrdersORM,tdict['uid'])
        sub_in_orm.lob_uid = str(tdict['lob_uid'])
        sub_in_orm.initiated_user_uid = str(tdict['initiated_user_uid'])
        sub_in_orm.plan_id =str(tdict['plan_id'])
        sub_in_orm.paid_amount = tdict['paid_amount']
        sub_in_orm.receipt_id = tdict['receipt_id']
        sub_in_orm.status = tdict['status']
        sub_in_orm.payment_id=tdict['payment_id']
        sub_in_orm.order_id=tdict['order_id']
        sub_in_orm.signature=tdict['signature']
        sub_in_orm.updated_date=tdict['updated_date']
        self.session.add(sub_in_orm)
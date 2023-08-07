from infrastructure.repository.base import AbstractRepository
from infrastructure.persistence.orm.models import PlansORM,SubscriptionORM,SubscriptionPaymentOrderORM
from domain.core.subscription import Plans, Subscription,SubscriptionPaymentOrder
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




class SubscriptionSQLAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, sub):
        sub_in_orm=SubscriptionORM(**sub.dict())
        self.session.add(sub_in_orm)
    
    def get(self, id):
         sub_in_orm=self.session.get(SubscriptionORM,str(id))
         if sub_in_orm is not None:
            return Subscription.from_orm(sub_in_orm)
         else:
             return None

    def list(self):
        sub_in_orm=self.session.query(SubscriptionORM).all()
        res=[]
        for s in sub_in_orm:
            res.append(Subscription.from_orm(s))
        return res

    def getByReference(self, **reference):
        sh_in_orm=self.session.query(SubscriptionORM).filter_by(**reference)
        res=[]
        for sh in sh_in_orm:
            res.append(Subscription.from_orm(sh))
        return res
    

    def delete(self,id):
        sub_in_orm=self.session.get(SubscriptionORM,str(id))
        self.session.delete(sub_in_orm)


    def update(self,user):
        tdict=user.dict()
        tdict['uid']=str(tdict['uid'])
        sub_in_orm=self.session.get(SubscriptionORM,tdict['uid'])
        sub_in_orm.lob_uid = str(tdict['lob_uid'])
        sub_in_orm.initiated_user_uid = str(tdict['initiated_user_uid'])
        sub_in_orm.plan_id =str(tdict['plan_id'])
        sub_in_orm.plan_start_date = tdict['plan_start_date']
        sub_in_orm.status = tdict['status']
        sub_in_orm.updated_date=tdict['updated_date']
        self.session.add(sub_in_orm)




class SubscriptionPaymentOrderSQLAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, sub):
        sub_in_orm=SubscriptionPaymentOrderORM(**sub.dict())
        self.session.add(sub_in_orm)
    
    def get(self, id):
         sub_in_orm=self.session.get(SubscriptionPaymentOrderORM,str(id))
         if sub_in_orm is not None:
            return SubscriptionPaymentOrder.from_orm(sub_in_orm)
         else:
             return None

    def list(self):
        sub_in_orm=self.session.query(SubscriptionPaymentOrderORM).all()
        res=[]
        for s in sub_in_orm:
            res.append(SubscriptionPaymentOrder.from_orm(s))
        return res

    def getByReference(self, **reference):
        sh_in_orm=self.session.query(SubscriptionPaymentOrderORM).filter_by(**reference)
        res=[]
        for sh in sh_in_orm:
            res.append(SubscriptionPaymentOrder.from_orm(sh))
        return res
    

    def delete(self,id):
        sub_in_orm=self.session.get(SubscriptionPaymentOrderORM,str(id))
        self.session.delete(sub_in_orm)


    def update(self,user):
        tdict=user.dict()
        tdict['uid']=str(tdict['uid'])
        sub_in_orm=self.session.get(SubscriptionPaymentOrderORM,tdict['uid'])
        sub_in_orm.subscription_uid = str(tdict['subscription_uid'])
        sub_in_orm.receipt_id = str(tdict['receipt_id'])
        sub_in_orm.payable_amount =str(tdict['payable_amount'])
        sub_in_orm.payment_id=tdict['payment_id']
        sub_in_orm.order_id=tdict['order_id']
        sub_in_orm.signature=tdict['signature']
        sub_in_orm.status = tdict['status']
        sub_in_orm.updated_date=tdict['updated_date']
        self.session.add(sub_in_orm)
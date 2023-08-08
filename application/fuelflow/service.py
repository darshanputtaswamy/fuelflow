from domain.core.subscription import Plans,Subscription,SubscriptionPaymentOrder, SubscriptionStatus,PlanType
import uuid
import datetime

'''
GET /lob   
GET /lob/{uid}
POST /lob
DELETE /lob
PUT /lob 

GET /lob/activities
GET /lob/activities/{lob_uid}
POST /lob/activities/{lob_uid}
DELETE /lob/activities


GET /lob/roles
GET /lob/roles/{lob_uid}
POST /lob/roles/{uid}
DELETE /lob/roles/{uid}

GET /lob/privilege
GET /lob/privilege/{lob_uid}
POST /lob/privilege/{uid}
DELETE /lob/privilege/{uid}

GET /lob/rota
GET /lob/rota/{lob_uid}
POST /lob/rota/{lob_uid}
PUT /lob/rota/{uid}
DELETE /lob/rota/{uid}


GET /lob/pos
GET /lob/pos/{lob_uid}
POST /lob/pos/{lob_uid}
PUT /lob/pos/{lob_uid}
DELETE /lob/pos/{uid}

'''

class FuelFlowService:
    def __init__(self,uow):
        self.uow=uow

    def create_lob(self,plan_type,plan_name,price,period,key,retention_limit,user_limit,status):
        created=datetime.datetime.now()            
        id=uuid.uuid4()
        plan=Plans(uid=str(id),plan_type=plan_type,plan_name=plan_name,price=price,period=period, key=key, retention_limit=retention_limit, user_limit=user_limit,status=status,created_date=created)

        with self.uow:
            self.uow.plans.add(plan)
            self.uow.commit()
            return id
        
    def update_lob(self,id,plan_type,plan_name,price,period,key,retention_limit,user_limit,status):
        with self.uow:
            plan = self.uow.plans.get(id) 
            if not plan:
                raise Exception("Plan "+plan+" not found")
            plan.plan_type=plan_type
            plan.plan_name=plan_name
            plan.price=price
            plan.period=period
            plan.key=key
            plan.retention_limit=retention_limit
            plan.user_limit=user_limit
            plan.status=status
            self.uow.plans.update(plan)
            self.uow.commit()
        

    def delete_lob(self,uid):
        with self.uow:
            plans = self.uow.plans.get(id=uid) 
            if not plans:
                raise Exception("Plan "+id+" not found")
            self.uow.plans.delete(uid)
            self.uow.commit()

    def hard_delete_lob(self,uid):
        with self.uow:
            plans = self.uow.plans.get(id=uid) 
            if not plans:
                raise Exception("Plan "+id+" not found")
            self.uow.plans.delete(uid)
            self.uow.commit()

    def get_lob_id(self):
        pass


    def get_lob_by_user_id(self,user_id):
        pass


    
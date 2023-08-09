from domain.core.subscription import Plans,Subscription,SubscriptionPaymentOrder, SubscriptionStatus,PlanType
from domain.fuelflow.store import Store,StoreActivities,StoreRoles,StoreUserPrivilege
import uuid
import datetime


class RolesService():
    def __init__(self,uow):
        self.uow=uow

    def create_role_type(self,store_uid,role_type):
        with self.uow:
            created=datetime.datetime.now()            
            uid=uuid.uuid4()
            store = self.uow.store.get(id=store_uid) 
            if not store:
                raise Exception("store "+store_uid+" not found")
            
            self.uow.store_roles.add(StoreRoles(uid=uid,store_uid=store_uid,roles=role_type))
            self.uow.commit()
        

    def delete_role_type(self,uid,store_uid):
        with self.uow:
            ac = self.uow.store_roles.getByReference(uid=uid,store_uid=store_uid) 
            if not ac:
                raise Exception("Activity record "+uid+" not found")
            self.uow.store_roles.delete(id=uid)
            self.uow.commit()
 

    def get_role_types_by_store(self,store_uid):
        with self.uow:
            store = self.uow.store.get(id=store_uid) 
            if not store:
                raise Exception("store "+store_uid+" not found")
            return self.uow.store_roles.getByReference(store_uid=store_uid) 
         
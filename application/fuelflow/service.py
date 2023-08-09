from domain.core.subscription import Plans,Subscription,SubscriptionPaymentOrder, SubscriptionStatus,PlanType
from domain.fuelflow.store import Store,StoreActivities,StoreRoles,StoreUserPrivilege
import uuid
import datetime
from .custom.privileges_service import PrivilegeService
from .custom.activity_service import ActivitiesService
from .custom.roles_service import RolesService

class FuelFlowService(PrivilegeService,ActivitiesService,RolesService):
    def __init__(self,uow):
        self.uow=uow
        super().__init__(uow)

    def create_store(self,buisness_name,type,address,postal_code,gst_number,user_uid):
        with self.uow:
            created=datetime.datetime.now()            
            store_id=uuid.uuid4()
            user = self.uow.user.get(id=user_uid)
            if not user:
                    raise Exception("User "+str(user_uid)+" not found")
            store=Store(uid=str(store_id),buisness_name=buisness_name,type=type,address=address,postal_code=postal_code, gst_number=gst_number, is_deleted='N', created_date=created)
            self.uow.store.add(store)
            self.uow.commit()
            self.create_privilege_record(user_uid=user_uid,store_uid=store_id,role='OWNER')
            return store
        
    def update_store_buisness_name(self,store_uid,buisness_name):
        with self.uow:
            updated=datetime.datetime.now() 
            store = self.uow.store.get(id=store_uid) 
            if not store:
                raise Exception("store "+store_uid+" not found")
            store.buisness_name=buisness_name
            store.updated_date=updated
            self.uow.store.update(store)
            self.uow.commit()

    def update_store_buisness_type(self,store_uid,type):
        with self.uow:
            updated=datetime.datetime.now() 
            store = self.uow.store.get(id=store_uid) 
            if not store:
                raise Exception("store "+store_uid+" not found")
            store.type=type
            store.updated_date=updated
            self.uow.store.update(store)
            self.uow.commit()
        
    def update_store_buisness_address(self,store_uid,address,postal_code):
        with self.uow:
            updated=datetime.datetime.now() 
            store = self.uow.store.get(id=store_uid) 
            if not store:
                raise Exception("store "+store_uid+" not found")
            store.address=address
            store.postal_code=postal_code
            store.updated_date=updated
            self.uow.store.update(store)
            self.uow.commit()

    def update_store_buisness_gst_number(self,store_uid,gst_number):
        with self.uow:
            updated=datetime.datetime.now()  
            store = self.uow.store.get(id=store_uid) 
            if not store:
                raise Exception("store "+store_uid+" not found")
            store.gst_number=gst_number
            store.updated_date=updated
            self.uow.store.update(store)
            self.uow.commit()

    def delete_store(self,uid):
        with self.uow:
            updated=datetime.datetime.now()  
            store = self.uow.store.get(id=uid) 
            if not store:
                raise Exception("Lob "+uid+" not found")
            store.deleted='Y'
            store.updated_date=updated
            self.uow.store.update(store)
            self.uow.commit()


    def hard_delete_store(self,uid):
        with self.uow:
            store = self.uow.store.get(id=uid) 
            if not store:
                raise Exception("store "+id+" not found")
            self.uow.store.delete(uid)
            self.uow.commit()

    def get_store_id(self,uid):
        with self.uow:
            store = self.uow.store.get(id=uid) 
            if not store:
                raise Exception("store "+uid+" not found")
            return store

    def get_store(self):
        with self.uow:
            store = self.uow.store.list()
            return store
    
    def get_store_by_user_id(self,user_id):
        with self.uow:
            user = self.uow.user.get(user_id)
            if not user:
                    raise Exception("User "+str(user_id)+" not found")
            records = self.get_privilege_record_by_user(user_id)
            res=[]
            for record in records:
                res.append( self.uow.store.get(record['store_uid']))
            return res

    
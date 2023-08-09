from domain.core.subscription import Plans,Subscription,SubscriptionPaymentOrder, SubscriptionStatus,PlanType
from domain.fuelflow.store import Store,StoreActivities,StoreRoles,StoreUserPrivilege
import uuid
import datetime


class CreditService():
    def __init__(self,uow):
        self.uow=uow

    def create_privilege_record(self,user_uid,store_uid,role):
        with self.uow:
            created=datetime.datetime.now()            
            uid=uuid.uuid4()
            user = self.uow.user.get(id=user_uid)
            if not user:
                    raise Exception("User "+str(user_uid)+" not found")
            store = self.uow.store.get(id=store_uid) 
            if not store:
                raise Exception("store "+store_uid+" not found")
            
            userPrivilege = self.uow.store_user_privileges.getByReference(store_uid=store_uid, user_uid=user_uid)
            if len(userPrivilege) >0 :
                raise Exception("User is already assosiated with store")
            
            userPrivilege=StoreUserPrivilege(uid=str(uid),user_uid=user_uid,store_uid=str(store_uid),role=role,created_date=created)
            self.uow.store_user_privileges.add(userPrivilege)
            self.uow.commit()
            return store
        
    def update_privilege_record(self,uid,user_uid,store_uid,role):
        with self.uow:
            updated=datetime.datetime.now() 
            user = self.uow.user.get(id=user_uid)
            if not user:
                raise Exception("User "+str(user_uid)+" not found")
            store = self.uow.store.get(id=store_uid) 
            if not store:
                raise Exception("store "+store_uid+" not found")
            userPrivilege = self.uow.store_user_privileges.get(id=uid) 
            if not userPrivilege:
                raise Exception("Privilege record "+uid+" not found")
            userPrivilege.role = role
            userPrivilege.updated_date=updated
            self.uow.store_user_privileges.update(userPrivilege)
            self.uow.commit()

    def delete_privilege_record(self,uid):
        with self.uow:
            userPrivilege = self.uow.store_user_privileges.get(id=uid) 
            if not userPrivilege:
                raise Exception("Privilege record "+uid+" not found")
            self.uow.store_user_privileges.delete(id=uid)
            self.uow.commit()
 

    def get_privilege_record_by_store(self,store_uid):
        with self.uow:
            store = self.uow.store.get(id=store_uid) 
            if not store:
                raise Exception("store "+store_uid+" not found")
            privs = self.uow.store_user_privileges.getByReference(store_uid=store_uid) 
            res=[]
            for priv in privs:
                 user = self.uow.user.get(id=priv.user_uid)
                 temp ={}
                 temp['uid']=priv.uid
                 temp['phone']=user.phone
                 temp['email']=user.email
                 temp['user_name']=user.username
                 temp['user_uid']=priv.user_uid
                 temp['store_uid']=priv.store_uid
                 temp['role']=priv.role
                 res.append(temp)
            return res
        
    def get_privilege_record_by_user(self,user_uid):
        with self.uow:
            user = self.uow.user.get(id=user_uid)
            if not user:
                    raise Exception("User "+str(user_uid)+" not found")
            privs = self.uow.store_user_privileges.getByReference(user_uid=user_uid) 
            res=[]
            for priv in privs:
                 store = self.uow.store.get(id=priv.store_uid)
                 temp ={}
                 temp['uid']=priv.uid
                 temp['phone']=user.phone
                 temp['email']=user.email
                 temp['user_name']=user.username
                 temp['store_uid']=priv.store_uid
                 temp['user_uid']=priv.user_uid
                 temp['buisness_name']=store.buisness_name
                 temp['gst_number']=store.gst_number
                 temp['type']=store.type
                 temp['address']=store.address + '  ' +store.postal_code
                 temp['role']=priv.role
                 res.append(temp)
            return res
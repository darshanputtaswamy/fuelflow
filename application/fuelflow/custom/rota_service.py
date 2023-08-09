from domain.core.subscription import Plans,Subscription,SubscriptionPaymentOrder, SubscriptionStatus,PlanType
from domain.fuelflow.store import Store,StoreActivities,StoreRoles,StoreUserPrivilege
import uuid
import datetime


class RotaService():
    def __init__(self,uow):
        self.uow=uow

    def create_rota_record(self,user_uid,store_uid,from_date,till_date,role_uid,activity_uid,approval_status):
        with self.uow:
            created=datetime.datetime.now()            
            uid=uuid.uuid4()
            user = self.uow.user.get(id=user_uid)
            if not user:
                    raise Exception("User "+str(user_uid)+" not found")
            store = self.uow.store.get(id=store_uid) 
            if not store:
                raise Exception("Store "+store_uid+" not found")
            
            activity = self.uow.store_activities.get(id=activity_uid) 
            if not activity:
                raise Exception("Activtiy "+activity_uid+" not found")
            
            role = self.uow.store_roles.get(id=role_uid) 
            if not role:
                raise Exception("Role "+role_uid+" not found")
            
            rota = self.uow.store_rota.getByReference(store_uid=store_uid, user_uid=user_uid)
            if len(rota) >0 :
                #logic check if not rata between from_date and till_date 
                raise Exception("User is already assosiated with rota")
            
            rota=StoreUserPrivilege(uid=str(uid),user_uid=user_uid,store_uid=store_uid,from_date=from_date,till_date=till_date,role_uid=role_uid,activity_uid=activity_uid,approval_status=approval_status,created_date=created)
            self.uow.store_rota.add(rota)
            self.uow.commit()
            return store
        
    def update_rota_record(self,uid,user_uid,store_uid,from_date,till_date,role_uid,activity_uid,approval_status):
        with self.uow:
            updated=datetime.datetime.now() 
            user = self.uow.user.get(id=user_uid)
            if not user:
                    raise Exception("User "+str(user_uid)+" not found")
            store = self.uow.store.get(id=store_uid) 
            if not store:
                raise Exception("Store "+store_uid+" not found")
            
            activity = self.uow.store_activities.get(id=activity_uid) 
            if not activity:
                raise Exception("Activtiy "+activity_uid+" not found")
            
            role = self.uow.store_roles.get(id=role_uid) 
            if not role:
                raise Exception("Role "+role_uid+" not found")
            
            rota = self.uow.store_rota.getByReference(store_uid=store_uid, user_uid=user_uid)
            if len(rota) >0 :
                #logic check if not rata between from_date and till_date 
                raise Exception("User is already assosiated with rota")
            rota.user_uid=user_uid
            rota.store_uid=store_uid
            rota.from_date=from_date
            rota.till_date=till_date
            rota.role_uid=role_uid
            rota.activity_uid=activity_uid
            rota.approval_status=approval_status
            rota.updated_date=updated
            self.uow.store_rota.update(rota)
            self.uow.commit()

    def delete_rota_record(self,uid):
        with self.uow:
            rota = self.uow.store_rota.get(id=uid) 
            if not rota:
                raise Exception("Rota record "+uid+" not found")
            self.uow.store_rota.delete(id=uid)
            self.uow.commit()
 

    def get_rota_record_by_store(self,store_uid):
        with self.uow:
            store = self.uow.store.get(id=store_uid) 
            if not store:
                raise Exception("store "+store_uid+" not found")
            privs = self.uow.store_rota.getByReference(store_uid=store_uid) 
            res=[]
            for priv in privs:
                 user = self.uow.user.get(id=priv.user_uid)
                 activity = self.uow.store_activities.get(id=priv.activity_uid) 
                 role = self.uow.store_roles.get(id=priv.role_uid) 
                 temp ={}
                 temp['uid']=priv.uid
                 temp['phone']=user.phone
                 temp['email']=user.email
                 temp['user_name']=user.username
                 temp['user_uid']=priv.user_uid
                 temp['store_uid']=priv.store_uid
                 temp['buisness_name']=priv.buisness_name
                 temp['type']=priv.type
                 temp['from_date']=priv.from_date
                 temp['till_date']=priv.till_date
                 temp['role_uid']=priv.role_uid
                 temp['role_type']=role.role_type
                 temp['activity_type']=activity.activity_type
                 temp['activity_uid']=priv.activity_uid
                 temp['approval_status']=priv.approval_status
                 temp['updated_date']=priv.updated_date
                 temp['created_date']=priv.created_date
                 res.append(temp)
            return res
        
    def get_rota_record_by_user(self,user_uid):
        with self.uow:
            user = self.uow.user.get(id=user_uid)
            if not user:
                    raise Exception("User "+str(user_uid)+" not found")
            privs = self.uow.store_user_privileges.getByReference(user_uid=user_uid) 
            res=[]
            for priv in privs:
                 store = self.uow.store.get(id=priv.store_uid)
                 activity = self.uow.store_activities.get(id=priv.activity_uid) 
                 role = self.uow.store_roles.get(id=priv.role_uid) 
                 temp ={}
                 temp['uid']=priv.uid
                 temp['phone']=user.phone
                 temp['email']=user.email
                 temp['user_name']=user.username
                 temp['user_uid']=priv.user_uid
                 temp['store_uid']=priv.store_uid
                 temp['buisness_name']=priv.buisness_name
                 temp['type']=priv.type
                 temp['from_date']=priv.from_date
                 temp['till_date']=priv.till_date
                 temp['role_uid']=priv.role_uid
                 temp['role_type']=role.role_type
                 temp['activity_type']=activity.activity_type
                 temp['activity_uid']=priv.activity_uid
                 temp['approval_status']=priv.approval_status
                 temp['updated_date']=priv.updated_date
                 temp['created_date']=priv.created_date
                 res.append(temp)
            return res
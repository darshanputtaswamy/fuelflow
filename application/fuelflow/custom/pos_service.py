from domain.core.subscription import Plans,Subscription,SubscriptionPaymentOrder, SubscriptionStatus,PlanType
from domain.fuelflow.store import Store,StoreActivities,StoreRoles,StoreUserPrivilege,POS
import uuid
import datetime


class POSService():
    def __init__(self,uow):
        self.uow=uow

    def create_store_pos(self,store_uid,pos_name,pos_type,pos_contact_uid,):
        with self.uow:
            created=datetime.datetime.now()            
            uid=uuid.uuid4()
            user = self.uow.user.get(id=pos_contact_uid)
            if not user:
                    raise Exception("User "+str(pos_contact_uid)+" not found")
            store = self.uow.store.get(id=store_uid) 
            if not store:
                raise Exception("store "+store_uid+" not found")
            
            pos = self.uow.store_pos.getByReference(store_uid=store_uid, pos_contact_uid=pos_contact_uid, pos_name=pos_name, pos_type=pos_type)
            if len(pos) >0 :
                raise Exception("POS already exists")
            pos=POS(uid=str(uid),store_uid=store_uid, pos_contact_uid=pos_contact_uid, pos_name=pos_name, pos_type=pos_type, created_date=created)
            self.uow.store_pos.add(pos)
            self.uow.commit()
            return store
        
    def update_pos(self,uid,store_uid,pos_name,pos_type,pos_contact_uid):
        with self.uow:
            updated=datetime.datetime.now() 
            user = self.uow.user.get(id=pos_contact_uid)
            if not user:
                raise Exception("User "+str(pos_contact_uid)+" not found")
            store = self.uow.store.get(id=store_uid) 
            if not store:
                raise Exception("store "+store_uid+" not found")
            pos = self.uow.store_pos.get(id=uid) 
            if not pos:
                raise Exception("POS record "+uid+" not found")
            pos.pos_name = pos_name
            pos.pos_type = pos_type
            pos.pos_contact_uid = pos_contact_uid
            pos.updated_date=updated
            self.uow.store_user_privileges.update(pos)
            self.uow.commit()

    def delete_pos(self,uid):
        with self.uow:
            pos = self.uow.store_pos.get(id=uid) 
            if not pos:
                raise Exception("POS "+uid+" not found")
            self.uow.store_pos.delete(id=uid)
            self.uow.commit()
 

    def get_pos_by_store(self,store_uid):
        with self.uow:
            store = self.uow.store.get(id=store_uid) 
            if not store:
                raise Exception("store "+store_uid+" not found")
            poss = self.uow.store_pos.getByReference(store_uid=store_uid) 
            res=[]
            for pos in poss:
                 user = self.uow.user.get(id=pos.pos_contact_uid)
                 temp ={}
                 temp['uid']=pos.uid
                 temp['pos_name']=pos.pos_name
                 temp['pos_type']=pos.pos_type
                 temp['pos_contact_uid']=pos.pos_contact_uid
                 temp['pos_contact_name']=user.username
                 temp['pos_contact_phone']=user.phone
                 temp['phone']=user.phone
                 temp['email']=user.email
                 temp['user_name']=user.username
                 temp['store_uid']=pos.store_uid
                 temp['buisness_name']=store.buisness_name
                 temp['gst_number']=store.gst_number
                 temp['type']=store.type
                 temp['address']=store.address + '  ' +store.postal_code
                 res.append(temp)
            return res
        
    def get_pos_by_user(self,user_uid):
        with self.uow:
            user = self.uow.user.get(id=user_uid)
            if not user:
                    raise Exception("User "+str(user_uid)+" not found")
            poss = self.uow.store_pos.getByReference(pos_contact_uid=user_uid) 
            res=[]
            for pos in poss:
                 store = self.uow.store.get(id=pos.store_uid)
                 temp ={}
                 temp['uid']=pos.uid
                 temp['pos_name']=pos.pos_name
                 temp['pos_type']=pos.pos_type
                 temp['pos_contact_uid']=pos.pos_contact_uid
                 temp['pos_contact_name']=user.username
                 temp['pos_contact_phone']=user.phone
                 temp['phone']=user.phone
                 temp['email']=user.email
                 temp['user_name']=user.username
                 temp['store_uid']=pos.store_uid
                 temp['buisness_name']=store.buisness_name
                 temp['gst_number']=store.gst_number
                 temp['type']=store.type
                 temp['address']=store.address + '  ' +store.postal_code
                 res.append(temp)
            return res
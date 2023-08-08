from domain.core.subscription import Plans,Subscription,SubscriptionPaymentOrder, SubscriptionStatus,PlanType
from domain.fuelflow.lob import LOB,LOBActivities,LOBRoles,LOBUserPrivilege
import uuid
import datetime


class PrivilegeService():
    def __init__(self,uow):
        self.uow=uow

    def create_privilege_record(self,user_uid,lob_uid,role):
        with self.uow:
            created=datetime.datetime.now()            
            uid=uuid.uuid4()
            user = self.uow.user.get(id=user_uid)
            if not user:
                    raise Exception("User "+str(user_uid)+" not found")
            lob = self.uow.lob.get(id=lob_uid) 
            if not lob:
                raise Exception("lob "+lob_uid+" not found")
            
            userPrivilege = self.uow.lob_user_privileges.getByReference(lob_uid=lob_uid, user_uid=user_uid)
            if len(userPrivilege) >0 :
                raise Exception("User is already assosiated with store")
            
            userPrivilege=LOBUserPrivilege(uid=str(uid),user_uid=user_uid,lob_uid=str(lob_uid),role=role,created_date=created)
            self.uow.lob_user_privileges.add(userPrivilege)
            self.uow.commit()
            return lob
        
    def update_privilege_record(self,uid,user_uid,lob_uid,role):
        with self.uow:
            updated=datetime.datetime.now() 
            user = self.uow.user.get(id=user_uid)
            if not user:
                raise Exception("User "+str(user_uid)+" not found")
            lob = self.uow.lob.get(id=lob_uid) 
            if not lob:
                raise Exception("lob "+lob_uid+" not found")
            userPrivilege = self.uow.lob_user_privileges.get(id=uid) 
            if not userPrivilege:
                raise Exception("Privilege record "+uid+" not found")
            userPrivilege.role = role
            userPrivilege.updated_date=updated
            self.uow.lob_user_privileges.update(userPrivilege)
            self.uow.commit()

    def delete_privilege_record(self,uid):
        with self.uow:
            userPrivilege = self.uow.lob_user_privileges.get(id=uid) 
            if not userPrivilege:
                raise Exception("Privilege record "+uid+" not found")
            self.uow.lob_user_privileges.delete(id=uid)
            self.uow.commit()
 

    def get_privilege_record_by_lob(self,lob_uid):
        with self.uow:
            lob = self.uow.lob.get(id=lob_uid) 
            if not lob:
                raise Exception("lob "+lob_uid+" not found")
            privs = self.uow.lob_user_privileges.getByReference(lob_uid=lob_uid) 
            res=[]
            for priv in privs:
                 user = self.uow.user.get(id=priv.user_uid)
                 temp ={}
                 temp['uid']=priv.uid
                 temp['phone']=user.phone
                 temp['email']=user.email
                 temp['user_name']=user.username
                 temp['user_uid']=priv.user_uid
                 temp['lob_uid']=priv.lob_uid
                 temp['role']=priv.role
                 res.append(temp)
            return res
        
    def get_privilege_record_by_user(self,user_uid):
        with self.uow:
            user = self.uow.user.get(id=user_uid)
            if not user:
                    raise Exception("User "+str(user_uid)+" not found")
            privs = self.uow.lob_user_privileges.getByReference(user_uid=user_uid) 
            res=[]
            for priv in privs:
                 lob = self.uow.lob.get(id=priv.lob_uid)
                 temp ={}
                 temp['uid']=priv.uid
                 temp['phone']=user.phone
                 temp['email']=user.email
                 temp['user_name']=user.username
                 temp['lob_uid']=priv.lob_uid
                 temp['user_uid']=priv.user_uid
                 temp['buisness_name']=lob.buisness_name
                 temp['gst_number']=lob.gst_number
                 temp['type']=lob.type
                 temp['address']=lob.address + '  ' +lob.postal_code
                 temp['role']=priv.role
                 res.append(temp)
            return res


    
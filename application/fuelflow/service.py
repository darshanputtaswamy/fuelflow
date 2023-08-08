from domain.core.subscription import Plans,Subscription,SubscriptionPaymentOrder, SubscriptionStatus,PlanType
from domain.fuelflow.lob import LOB,LOBActivities,LOBRoles,LOBUserPrivilege
import uuid
import datetime


class FuelFlowService:
    def __init__(self,uow):
        self.uow=uow

    def create_lob(self,buisness_name,type,address,postal_code,gst_number,user_uid):
        with self.uow:
            created=datetime.datetime.now()            
            lob_id=uuid.uuid4()
            uid=uuid.uuid4()
            user = self.uow.user.get(id=user_uid)
            if not user:
                    raise Exception("User "+str(user_uid)+" not found")
            lob=LOB(uid=str(lob_id),buisness_name=buisness_name,type=type,address=address,postal_code=postal_code, gst_number=gst_number, is_deleted='N', created_date=created)
            userPrivilege=LOBUserPrivilege(uid=str(uid),user_uid=user_uid,lob_uid=str(lob_id),role='OWNER',created_date=created)
            self.uow.lob.add(lob)
            self.uow.commit()
            self.uow.lob_user_privileges.add(userPrivilege)
            self.uow.commit()
            return lob
        
    def update_lob_buisness_name(self,lob_uid,buisness_name):
        with self.uow:
            updated=datetime.datetime.now() 
            lob = self.uow.lob.get(id=lob_uid) 
            if not lob:
                raise Exception("lob "+lob_uid+" not found")
            lob.buisness_name=buisness_name
            lob.updated_date=updated
            self.uow.lob.update(lob)
            self.uow.commit()

    def update_lob_buisness_type(self,lob_uid,type):
        with self.uow:
            updated=datetime.datetime.now() 
            lob = self.uow.lob.get(id=lob_uid) 
            if not lob:
                raise Exception("lob "+lob_uid+" not found")
            lob.type=type
            lob.updated_date=updated
            self.uow.lob.update(lob)
            self.uow.commit()
        
    def update_lob_buisness_address(self,lob_uid,address,postal_code):
        with self.uow:
            updated=datetime.datetime.now() 
            lob = self.uow.lob.get(id=lob_uid) 
            if not lob:
                raise Exception("lob "+lob_uid+" not found")
            lob.address=address
            lob.postal_code=postal_code
            lob.updated_date=updated
            self.uow.lob.update(lob)
            self.uow.commit()

    def update_lob_buisness_gst_number(self,lob_uid,gst_number):
        with self.uow:
            updated=datetime.datetime.now()  
            lob = self.uow.lob.get(id=lob_uid) 
            if not lob:
                raise Exception("lob "+lob_uid+" not found")
            lob.gst_number=gst_number
            lob.updated_date=updated
            self.uow.lob.update(lob)
            self.uow.commit()

    def delete_lob(self,uid):
        with self.uow:
            updated=datetime.datetime.now()  
            lob = self.uow.lob.get(id=uid) 
            if not lob:
                raise Exception("Lob "+uid+" not found")
            lob.deleted='Y'
            lob.updated_date=updated
            self.uow.lob.update(lob)
            self.uow.commit()


    def hard_delete_lob(self,uid):
        with self.uow:
            lob = self.uow.lob.get(id=uid) 
            if not lob:
                raise Exception("lob "+id+" not found")
            self.uow.lob.delete(uid)
            self.uow.commit()

    def get_lob_id(self,uid):
        with self.uow:
            lob = self.uow.lob.get(id=uid) 
            if not lob:
                raise Exception("lob "+uid+" not found")
            return lob

    def get_lob(self):
        with self.uow:
            lob = self.uow.lob.list()
            return lob
    
    def get_lob_by_user_id(self,user_id):
        with self.uow:
            user = self.uow.user.get(user_id)
            if not user:
                    raise Exception("User "+str(user_id)+" not found")
            records = self.uow.lob_user_privileges.getByReference(user_uid=user_id)
            res=[]
            for record in records:
                res.append( self.uow.lob.get(record.lob_uid))
            return res

    
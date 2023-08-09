from infrastructure.repository.base import AbstractRepository
from infrastructure.persistence.orm.models import StoreORM,StoreActivitiesORM,StoreRolesORM,StoreRotaORM,StoreUserPrivilegeORM,POSORM
from domain.fuelflow.store import Store,StoreActivities,StoreRoles,StoreRota,StoreUserPrivilege,POS
from sqlalchemy.orm import load_only




class StoreSQLAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, store):
        store_in_orm=StoreORM(**store.dict())
        self.session.add(store_in_orm)

    def getByReference(self, **reference):
        sh_in_orm=self.session.query(StoreORM).filter_by(**reference)
        res=[]
        for sh in sh_in_orm:
            res.append(Store.from_orm(sh))
        return res
    
    def get(self, id):
         store_in_orm=self.session.get(StoreORM,str(id))
         if store_in_orm is not None:
            return Store.from_orm(store_in_orm)
         else:
             return None

    def list(self):
        store_in_orm=self.session.query(StoreORM).all()
        res=[]
        for RCA in store_in_orm:
            res.append(Store.from_orm(RCA))
        return res
        

    def delete(self,id):
        store_in_orm=self.session.get(StoreORM,str(id))
        self.session.delete(store_in_orm)

    def update(self,user):
        tdict=user.dict()
        tdict['uid']=str(tdict['uid'])
        store_in_orm=self.session.get(StoreORM,tdict['uid'])
        store_in_orm.buisness_name = tdict['buisness_name']
        store_in_orm.type = tdict['type']
        store_in_orm.address =tdict['address']
        store_in_orm.postal_code = tdict['postal_code']
        store_in_orm.is_deleted = tdict['is_deleted']
        store_in_orm.gst_number = tdict['gst_number']
        store_in_orm.updated_date=tdict['updated_date']
        self.session.add(store_in_orm)




class StoreActivitiesSQLAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, activtiy):
        activtiy_in_orm=StoreActivitiesORM(**activtiy.dict())
        self.session.add(activtiy_in_orm)
    
    def get(self, id):
         activtiy_in_orm=self.session.get(StoreActivitiesORM,str(id))
         if activtiy_in_orm is not None:
            return StoreActivities.from_orm(activtiy_in_orm)
         else:
             return None

    def list(self):
        activtiy_in_orm=self.session.query(StoreActivitiesORM).all()
        res=[]
        for RCA in activtiy_in_orm:
            res.append(StoreActivities.from_orm(RCA))
        return res

    def getByReference(self, **reference):
        sh_in_orm=self.session.query(StoreActivitiesORM).filter_by(**reference)
        res=[]
        for sh in sh_in_orm:
            res.append(StoreActivities.from_orm(sh))

        return res

    def delete(self,id):
        activtiy_in_orm=self.session.get(StoreActivitiesORM,str(id))
        self.session.delete(activtiy_in_orm)

    def update(self):
         raise NotImplementedError



class StoreRolesSQLAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, store):
        store_in_orm=StoreRolesORM(**store.dict())
        self.session.add(store_in_orm)
    
    def get(self, id):
         store_in_orm=self.session.get(StoreRolesORM,str(id))
         if store_in_orm is not None:
            return StoreRoles.from_orm(store_in_orm)
         else:
             return None
         
    def getByReference(self, **reference):
        sh_in_orm=self.session.query(StoreRolesORM).filter_by(**reference)
        res=[]
        for sh in sh_in_orm:
            res.append(StoreRoles.from_orm(sh))
        return res
    

    def list(self):
        store_in_orm=self.session.query(StoreRolesORM).all()
        res=[]
        for RCA in store_in_orm:
            res.append(StoreRoles.from_orm(RCA))
        return res


    def delete(self,id):
        store_in_orm=self.session.get(StoreRolesORM,str(id))
        self.session.delete(store_in_orm)

    def update(self):
        raise NotImplementedError

class StoreUserPrivilegeSQLAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, store):
        store_in_orm=StoreUserPrivilegeORM(**store.dict())
        self.session.add(store_in_orm)

    def getByReference(self, **reference):
        sh_in_orm=self.session.query(StoreUserPrivilegeORM).filter_by(**reference)
        res=[]
        for sh in sh_in_orm:
            res.append(StoreUserPrivilege.from_orm(sh))
        return res
    
    def get(self, id):
         store_in_orm=self.session.get(StoreUserPrivilegeORM,str(id))
         if store_in_orm is not None:
            return StoreUserPrivilege.from_orm(store_in_orm)
         else:
             return None

    def list(self):
        store_in_orm=self.session.query(StoreUserPrivilegeORM).all()
        res=[]
        for RCA in store_in_orm:
            res.append(StoreUserPrivilege.from_orm(RCA))
        return res
        

    def delete(self,id):
        store_in_orm=self.session.get(StoreUserPrivilegeORM,str(id))
        self.session.delete(store_in_orm)

    def update(self,user):
        tdict=user.dict()
        tdict['uid']=str(tdict['uid'])
        store_in_orm=self.session.get(StoreUserPrivilegeORM,str(tdict['uid']))
        store_in_orm.user_uid = str(tdict['user_uid'])
        store_in_orm.store_uid = str(tdict['store_uid'])
        store_in_orm.role =tdict['role']
        store_in_orm.updated_date=tdict['updated_date']
        self.session.add(store_in_orm)



class StoreRotaSQLAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, store):
        store_in_orm=StoreRotaORM(**store.dict())
        self.session.add(store_in_orm)

    def getByReference(self, **reference):
        sh_in_orm=self.session.query(StoreRotaORM).filter_by(**reference)
        res=[]
        for sh in sh_in_orm:
            res.append(StoreRota.from_orm(sh))
        return res
    
    def get(self, id):
         store_in_orm=self.session.get(StoreRotaORM,str(id))
         if store_in_orm is not None:
            return StoreRota.from_orm(store_in_orm)
         else:
             return None

    def list(self):
        store_in_orm=self.session.query(StoreRotaORM).all()
        res=[]
        for RCA in store_in_orm:
            res.append(StoreRota.from_orm(RCA))
        return res
        

    def delete(self,id):
        store_in_orm=self.session.get(StoreRotaORM,str(id))
        self.session.delete(store_in_orm)

    def update(self,user):
        tdict=user.dict()
        tdict['uid']=str(tdict['uid'])
        store_in_orm=self.session.get(StoreRotaORM,tdict['uid'])
        store_in_orm.store_uid = str(tdict['store_uid'])
        store_in_orm.user_uid = str(tdict['user_uid'])
        store_in_orm.from_date =tdict['from_date']
        store_in_orm.till_date=tdict['till_date']
        store_in_orm.role_uid=str(tdict['role_uid'])
        store_in_orm.activity_uid=str(tdict['activity_uid'])
        store_in_orm.approval_status=tdict['approval_status']
        self.session.add(store_in_orm)


class POSSQLAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, store):
        store_in_orm=POSORM(**store.dict())
        self.session.add(store_in_orm)

    def getByReference(self, **reference):
        sh_in_orm=self.session.query(POSORM).filter_by(**reference)
        res=[]
        for sh in sh_in_orm:
            res.append(POS.from_orm(sh))
        return res
    
    def get(self, id):
         store_in_orm=self.session.get(POSORM,str(id))
         if store_in_orm is not None:
            return POS.from_orm(store_in_orm)
         else:
             return None

    def list(self):
        store_in_orm=self.session.query(POSORM).all()
        res=[]
        for RCA in store_in_orm:
            res.append(POS.from_orm(RCA))
        return res
        

    def delete(self,id):
        store_in_orm=self.session.get(POSORM,str(id))
        self.session.delete(store_in_orm)

    def update(self,user):
        tdict=user.dict()
        tdict['uid']=str(tdict['uid'])
        store_in_orm=self.session.get(POSORM,tdict['uid'])
        store_in_orm.store_uid = str(tdict['store_uid'])
        store_in_orm.pos_name = str(tdict['pos_name'])
        store_in_orm.pos_type =tdict['pos_type']
        store_in_orm.pos_contact_uid=str(tdict['pos_contact_uid'])
        store_in_orm.updated_date=tdict['updated_date']
        self.session.add(store_in_orm)
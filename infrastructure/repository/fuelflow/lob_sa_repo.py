from infrastructure.repository.base import AbstractRepository
from infrastructure.persistence.orm.models import LOBORM,LOBActivitiesORM,LOBRolesORM,LOBRotaORM,LOBUserPrivilegeORM,POSORM
from domain.fuelflow.lob import LOB,LOBActivities,LOBRoles,LOBRota,LOBUserPrivilege,POS
from sqlalchemy.orm import load_only




class LOBSQLAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, lob):
        lob_in_orm=LOBORM(**lob.dict())
        self.session.add(lob_in_orm)

    def getByReference(self, **reference):
        sh_in_orm=self.session.query(LOBORM).filter_by(**reference)
        res=[]
        for sh in sh_in_orm:
            res.append(LOB.from_orm(sh))
        return res
    
    def get(self, id):
         lob_in_orm=self.session.get(LOBORM,str(id))
         if lob_in_orm is not None:
            return LOB.from_orm(lob_in_orm)
         else:
             return None

    def list(self):
        lob_in_orm=self.session.query(LOBORM).all()
        res=[]
        for RCA in lob_in_orm:
            res.append(LOB.from_orm(RCA))
        return res
        

    def delete(self,id):
        lob_in_orm=self.session.get(LOBORM,str(id))
        self.session.delete(lob_in_orm)

    def update(self,user):
        tdict=user.dict()
        tdict['uid']=str(tdict['uid'])
        lob_in_orm=self.session.get(LOBORM,tdict['uid'])
        lob_in_orm.buisness_name = tdict['buisness_name']
        lob_in_orm.type = tdict['type']
        lob_in_orm.address =tdict['address']
        lob_in_orm.postal_code = tdict['postal_code']
        lob_in_orm.is_deleted = tdict['is_deleted']
        lob_in_orm.updated_date=tdict['updated_date']
        self.session.add(lob_in_orm)




class LOBActivitiesSQLAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, lob):
        lob_in_orm=LOBActivitiesORM(**lob.dict())
        self.session.add(lob_in_orm)
    
    def get(self, id):
         lob_in_orm=self.session.get(LOBActivitiesORM,str(id))
         if lob_in_orm is not None:
            return LOBActivities.from_orm(lob_in_orm)
         else:
             return None

    def list(self):
        lob_in_orm=self.session.query(LOBActivitiesORM).all()
        res=[]
        for RCA in lob_in_orm:
            res.append(LOBActivities.from_orm(RCA))
        return res

    def getByReference(self, **reference):
        sh_in_orm=self.session.query(LOBActivitiesORM).filter_by(**reference)
        res=[]
        for sh in sh_in_orm:
            res.append(LOBActivities.from_orm(sh))

        return res

    def delete(self,id):
        lob_in_orm=self.session.get(LOBActivitiesORM,str(id))
        self.session.delete(lob_in_orm)

    def update(self):
         raise NotImplementedError



class LOBRolesSQLAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, lob):
        lob_in_orm=LOBRolesORM(**lob.dict())
        self.session.add(lob_in_orm)
    
    def get(self, id):
         lob_in_orm=self.session.get(LOBRolesORM,str(id))
         if lob_in_orm is not None:
            return LOBRoles.from_orm(lob_in_orm)
         else:
             return None
         
    def getByReference(self, **reference):
        sh_in_orm=self.session.query(LOBRolesORM).filter_by(**reference)
        res=[]
        for sh in sh_in_orm:
            res.append(LOBRoles.from_orm(sh))
        return res
    

    def list(self):
        lob_in_orm=self.session.query(LOBRolesORM).all()
        res=[]
        for RCA in lob_in_orm:
            res.append(LOBRoles.from_orm(RCA))
        return res


    def delete(self,id):
        lob_in_orm=self.session.get(LOBRolesORM,str(id))
        self.session.delete(lob_in_orm)

    def update(self):
        raise NotImplementedError

class LOBUserPrivilegeSQLAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, lob):
        lob_in_orm=LOBUserPrivilegeORM(**lob.dict())
        self.session.add(lob_in_orm)

    def getByReference(self, **reference):
        sh_in_orm=self.session.query(LOBUserPrivilegeORM).filter_by(**reference)
        res=[]
        for sh in sh_in_orm:
            res.append(LOBUserPrivilege.from_orm(sh))
        return res
    
    def get(self, id):
         lob_in_orm=self.session.get(LOBUserPrivilegeORM,str(id))
         if lob_in_orm is not None:
            return LOBUserPrivilege.from_orm(lob_in_orm)
         else:
             return None

    def list(self):
        lob_in_orm=self.session.query(LOBUserPrivilegeORM).all()
        res=[]
        for RCA in lob_in_orm:
            res.append(LOBUserPrivilege.from_orm(RCA))
        return res
        

    def delete(self,id):
        lob_in_orm=self.session.get(LOBUserPrivilegeORM,str(id))
        self.session.delete(lob_in_orm)

    def update(self,user):
        tdict=user.dict()
        tdict['uid']=str(tdict['uid'])
        lob_in_orm=self.session.get(LOBUserPrivilegeORM,str(tdict['uid']))
        lob_in_orm.user_uid = str(tdict['user_uid'])
        lob_in_orm.lob_uid = str(tdict['lob_uid'])
        lob_in_orm.role =tdict['role']
        lob_in_orm.updated_date=tdict['updated_date']
        self.session.add(lob_in_orm)



class LOBRotaSQLAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, lob):
        lob_in_orm=LOBRotaORM(**lob.dict())
        self.session.add(lob_in_orm)

    def getByReference(self, **reference):
        sh_in_orm=self.session.query(LOBRotaORM).filter_by(**reference)
        res=[]
        for sh in sh_in_orm:
            res.append(LOBRota.from_orm(sh))
        return res
    
    def get(self, id):
         lob_in_orm=self.session.get(LOBRotaORM,str(id))
         if lob_in_orm is not None:
            return LOBRota.from_orm(lob_in_orm)
         else:
             return None

    def list(self):
        lob_in_orm=self.session.query(LOBRotaORM).all()
        res=[]
        for RCA in lob_in_orm:
            res.append(LOBRota.from_orm(RCA))
        return res
        

    def delete(self,id):
        lob_in_orm=self.session.get(LOBRotaORM,str(id))
        self.session.delete(lob_in_orm)

    def update(self,user):
        tdict=user.dict()
        tdict['uid']=str(tdict['uid'])
        lob_in_orm=self.session.get(LOBRotaORM,tdict['uid'])
        lob_in_orm.lob_uid = str(tdict['lob_uid'])
        lob_in_orm.user_uid = str(tdict['user_uid'])
        lob_in_orm.from_date =tdict['from_date']
        lob_in_orm.till_date=tdict['till_date']
        lob_in_orm.role_uid=str(tdict['role_uid'])
        lob_in_orm.activity_uid=str(tdict['activity_uid'])
        lob_in_orm.approval_status=tdict['approval_status']
        self.session.add(lob_in_orm)


class POSSQLAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, lob):
        lob_in_orm=POSORM(**lob.dict())
        self.session.add(lob_in_orm)

    def getByReference(self, **reference):
        sh_in_orm=self.session.query(POSORM).filter_by(**reference)
        res=[]
        for sh in sh_in_orm:
            res.append(POS.from_orm(sh))
        return res
    
    def get(self, id):
         lob_in_orm=self.session.get(POSORM,str(id))
         if lob_in_orm is not None:
            return POS.from_orm(lob_in_orm)
         else:
             return None

    def list(self):
        lob_in_orm=self.session.query(POSORM).all()
        res=[]
        for RCA in lob_in_orm:
            res.append(POS.from_orm(RCA))
        return res
        

    def delete(self,id):
        lob_in_orm=self.session.get(POSORM,str(id))
        self.session.delete(lob_in_orm)

    def update(self,user):
        tdict=user.dict()
        tdict['uid']=str(tdict['uid'])
        lob_in_orm=self.session.get(POSORM,tdict['uid'])
        lob_in_orm.lob_uid = str(tdict['lob_uid'])
        lob_in_orm.pos_name = str(tdict['pos_name'])
        lob_in_orm.pos_type =tdict['pos_type']
        lob_in_orm.pos_contact_uid=str(tdict['pos_contact_uid'])
        lob_in_orm.updated_date=tdict['updated_date']
        self.session.add(lob_in_orm)
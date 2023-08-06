from infrastructure.repository.base import AbstractRepository
from infrastructure.persistence.orm.models import AppUsersORM,AppUserVerificationORM
from domain.core.app_users import AppUsers,AppUserVerification
from sqlalchemy.orm import load_only

import random
import string


class AppUsersSQLAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, user):
        user_in_orm=AppUsersORM(**user.dict())
        self.session.add(user_in_orm)

    def getByReference(self, **reference):
        sh_in_orm=self.session.query(AppUsersORM).filter_by(**reference)
        res=[]
        for sh in sh_in_orm:
            res.append(AppUsers.from_orm(sh))
        return res
    
    def get(self, id):
         user_in_orm=self.session.get(AppUsersORM,str(id))
         if user_in_orm is not None:
            return AppUsers.from_orm(user_in_orm)
         else:
             return None

    def list(self):
        user_in_orm=self.session.query(AppUsersORM).all()
        res=[]
        for RCA in user_in_orm:
            res.append(AppUsers.from_orm(RCA))
        return res
        

    def delete(self,id):
        user_in_orm=self.session.get(AppUsersORM,str(id))
        self.session.delete(user_in_orm)


    def getVerificationCode(self,user_uid):
        uv_in_orm=self.session.query(AppUserVerificationORM).filter_by(user_uid=str(user_uid))
        res=[]
        for uv in uv_in_orm:
            res.append(AppUserVerification.from_orm(uv))
        return res

    def saveVerificationCode(self,user_verification_code):
        uv_in_orm=AppUserVerificationORM(**user_verification_code.dict())
        self.session.add(uv_in_orm)
        
    def deleteVerificationCode(self,uid):
        uv_in_orm=self.session.get(AppUserVerificationORM,str(uid))
        self.session.delete(uv_in_orm)

    def update(self,user):
        tdict=user.dict()
        tdict['uid']=str(tdict['uid'])
        user_in_orm=self.session.get(AppUsersORM,tdict['uid'])
        user_in_orm.username = tdict['username']
        user_in_orm.phone = tdict['phone']
        user_in_orm.email =tdict['email']
        user_in_orm.password = tdict['password']
        user_in_orm.user_type = tdict['user_type']
        user_in_orm.is_locked = tdict['is_locked']
        user_in_orm.is_verified=tdict['is_verified']
        user_in_orm.is_deleted=tdict['is_deleted']
        self.session.add(user_in_orm)


  
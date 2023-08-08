from domain.core.app_users import AppUsers,AppUserVerification
import uuid
import datetime

class UserService:
    def __init__(self,uow):
        self.uow=uow

    def get_user_by_id(self,uid):
        with self.uow:
            existing_user= self.uow.user.get(id=uid) 
            if  not existing_user:
                raise Exception("user not found")
        return existing_user 
    
    def get_users(self):
        with self.uow:
            existing_user= self.uow.user.list() 
            if len(existing_user) == 0:
                raise Exception("users not found")
        return existing_user

    def get_user_by_email(self,email):
        with self.uow:
            existing_user= self.uow.user.getByReference(email=email) 
            if len(existing_user) == 0:
                raise Exception("user not found")
        return existing_user[0]    


    def get_user_by_phone(self,phone):
        with self.uow:
            existing_user= self.uow.user.getByReference(phone=phone) 
            if len(existing_user) == 0:
                raise Exception("user not found")
        return existing_user[0]    

    def add_user(self,username,phone,email,password):
      
        with self.uow:
            existing_user= self.uow.user.getByReference(phone=phone) 
            if len(existing_user) != 0:
                raise Exception("Phone "+phone+" already exist")
            
            existing_user= self.uow.user.getByReference(email=email) 
            if len(existing_user) != 0:
                raise Exception("Email "+email+" already exist")
            id=uuid.uuid4()
            created=datetime.datetime.now()
            self.uow.user.add(AppUsers(uid=id,
                                       username=username,
                                       phone=phone,
                                       email=email,
                                       password=password,
                                       user_type='U',
                                       is_locked='N',
                                       is_verified='N',
                                       is_deleted="N",
                                       created_date=created
                                       ))
            self.uow.commit()
            return id
    
    def hard_delete_user(self,user_id):
        with self.uow:
            existing_user = self.uow.user.get(user_id) 
            if not existing_user:
                raise Exception("User "+user_id+" not found")
            self.uow.user.delete(user_id)
            self.uow.commit()


    def delete_user(self,user_id):

        with self.uow:
            existing_user = self.uow.user.get(user_id) 
            if not existing_user:
                raise Exception("User "+user_id+" not found")
            userObject = existing_user
            userObject.is_deleted='Y'
            self.uow.user.update(userObject)
            self.uow.commit()

    def lock_user(self,user_id,status):

        with self.uow:
            existing_user = self.uow.user.get(user_id) 
            if not existing_user:
                raise Exception("User "+user_id+" not found")
            userObject = existing_user
            userObject.is_locked=status
            self.uow.user.update(userObject)
            self.uow.commit()

    def is_verified(self,user_id):

        with self.uow:
            existing_user = self.uow.user.get(user_id) 
            if not existing_user:
                raise Exception("User "+user_id+" not found")
            userObject = existing_user
            userObject.is_verified='Y'
            self.uow.user.update(userObject)
            self.uow.commit()


    def update_user_type(self,user_id,value):

        with self.uow:
            existing_user = self.uow.user.get(user_id)
            if not existing_user:
                raise Exception("User "+user_id+" not found")
            userObject = existing_user
            userObject.user_type=value
            self.uow.user.update(userObject)
            self.uow.commit()

    def update_user_password(self,user_id,password):
        print("called")
        with self.uow:
            existing_user = self.uow.user.get(user_id) 
            if not existing_user:
                raise Exception("User "+user_id+" not found")
            userObject = existing_user
            userObject.password=password
            self.uow.user.update(userObject)
            self.uow.commit()

    def update_username(self,user_id,username):

        with self.uow:
            existing_user = self.uow.user.get(user_id) 
            if not existing_user:
                raise Exception("User "+user_id+" not found")
            userObject = existing_user
            userObject.username=username
            self.uow.user.update(userObject)
            self.uow.commit()


    def get_user_verification_code(self,user_id):

        with self.uow:
            existing_user = self.uow.user.get(user_id)
            if not existing_user:
                raise Exception("User "+user_id+" not found")
            
            existing_user_verification_code = self.uow.user.getVerificationCode(user_uid=user_id) 

            if len(existing_user_verification_code) == 0:
                raise Exception("User verification for "+user_id+" not found")

            uvObject = existing_user_verification_code[0]
            return uvObject.verification_code
        

    def save_user_verification_code(self,user_id,verification_code):
        with self.uow:
            id=uuid.uuid4()
            existing_user = self.uow.user.get(user_id)
            if not existing_user:
                raise Exception("User "+user_id+" not found")
            self.__delete_user_verification_code(str(user_id))
            self.uow.user.saveVerificationCode(AppUserVerification(uid=id,user_uid=str(user_id),verification_code=verification_code))
            self.uow.commit()
            return id
        

    def __delete_user_verification_code(self,user_id):
        
        with self.uow:
            existing_user = self.uow.user.get(user_id)
            if not existing_user:
                raise Exception("User "+user_id+" not found")
            
            existing_user_verification_code = self.uow.user.getVerificationCode(user_uid=user_id) 
            if len(existing_user_verification_code) == 0:
                return True
            
            for uv in existing_user_verification_code:
                self.uow.user.deleteVerificationCode(uid=uv.uid) 

            self.uow.commit()
            return True
        
 
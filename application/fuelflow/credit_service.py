from domain.core.permission import Permission
import uuid

class PermissionManager:
    def __init__(self,uow):
        self.uow=uow

    def add_user(self,rca_id,shared_user,user_id):
        id=uuid.uuid4()
        with self.uow:
            existing_rca = self.uow.rca.getByReference(id=rca_id) 
            if len(existing_rca) == 0:
                raise Exception("RCA with id ["+rca_id+"] does not exist to add comment")
            rcaObject = existing_rca[0]
            if rcaObject.owner != user_id:
                raise Exception(user_id +" does not have privilege to update RCA with id ["+rca_id+"]")
            existing_user_for_rca = self.uow.permissions.getByReference(user_id=shared_user) 
            if len(existing_user_for_rca) != 0:
                raise Exception("User already exist for selected ["+rca_id+"]")
            self.uow.permissions.add(Permission(id=id,rca_id=rca_id,user_id=shared_user))
            self.uow.commit()
        return id

    def delete_user(self,rca_id,id,user_id):

        with self.uow:
            existing_rca = self.uow.rca.getByReference(id=rca_id) 
            if len(existing_rca) == 0:
                raise Exception("RCA with id ["+rca_id+"] not found")
            rcaObject = existing_rca[0]
            if rcaObject.owner != user_id:
                raise Exception(user_id +" does not have privilege to update RCA with id ["+rca_id+"]")    
            existing_permission = self.uow.permissions.getByReference(id=id,rca_id=rca_id) 
            if len(existing_permission) == 0:
                raise Exception("User already not assosiated with rca ["+id+"]")
            self.uow.permissions.delete(id=id)
            self.uow.commit()

 

    def list_user_for_rca(self,rca_id):
        with self.uow:
            return self.uow.permissions.getByReference(rca_id=rca_id) 

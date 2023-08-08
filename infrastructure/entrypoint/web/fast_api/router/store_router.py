from fastapi import APIRouter
from fastapi import Depends,FastAPI, Form,Request,status, HTTPException,Response,File, UploadFile
from infrastructure.persistence.database.DatabaseSessionFactory import DatabaseSessionFactory
from application.unit_of_work import SqlAlchemyUnitOfWork
from application.fuelflow.service import FuelFlowService
from fastapi.responses import JSONResponse
from ..exception import CustomHTTPException
from .store_sub_routers.unload_router import unload_router
from .store_sub_routers.credit_router import credit_router
from .store_sub_routers.registry_router import registry_router

sqlaclk_uow= SqlAlchemyUnitOfWork(DatabaseSessionFactory)
store_router = APIRouter()
store_service=FuelFlowService(sqlaclk_uow)


'''
GET /store/activities
GET /store/activities/{store_uid}
POST /store/activities/{store_uid}
DELETE /store/activities


GET /store/previlege
GET /store/previlege/{store_uid}
POST /store/previlege/{uid}
DELETE /store/previlege/{uid}


GET /store/roles
GET /store/roles/{store_uid}
POST /store/roles/{uid}
DELETE /store/roles/{uid}


GET /store/rota
GET /store/rota/{store_uid}
POST /store/rota/{store_uid}
PUT /store/rota/{uid}
DELETE /store/rota/{uid}


GET /store/pos
GET /store/pos/{store_uid}
POST /store/pos/{store_uid}
PUT /store/pos/{store_uid}
DELETE /store/pos/{uid}

'''

@store_router.get("/all")
async def list_all_store():
    # Get user logic here
    try:

        store=store_service.get_store()
        return store
    
    except Exception as e:
        raise CustomHTTPException(message=e)



@store_router.get("/by-user/{user_id}")
async def  list_stores_associated_with_user_id(user_id:str):
    # Get user logic here
    try:
        stores=store_service.get_store_by_user_id(user_id)
        return stores
    except Exception as e:
        raise CustomHTTPException(message=e)


@store_router.post("/")
async def create_new_store(
    buisness_name: str = Form(...), 
    type: str = Form(...), 
    address: str = Form(...), 
    postal_code: str = Form(...), 
    gst_number: str = Form(...), 
    user_uid: str = Form(...), 
):
    try:
        store=store_service.create_store(buisness_name,type,address,postal_code,gst_number,user_uid)
        return {"message": f"Store created successfully for user ID {store.uid}"}
    except Exception as e:
        raise CustomHTTPException(message=e)



@store_router.delete("/{id}")
async def delete_user(id: str):
    try:
        users=store_service.hard_delete_store(uid=id)
        print("after return")
        return {"message": f"Lob {id} deleted successfully"}
    except Exception as e:
        raise CustomHTTPException(message=e)
    


@store_router.get("/{store_id}")
async def get_store_details(store_id: str):
    # Get user logic here
    try:

        user=store_service.get_store_id(uid=store_id)
        return user
    
    except Exception as e:
        raise CustomHTTPException(message=e)



#TODO: get rid of id from url instead use jwt token
@store_router.put("/store_name")
async def update_store_name(store_uid:str=  Form(...), buisness_name:str = Form(...)):
    try:
        store_service.update_store_buisness_name(store_uid=store_uid,buisness_name=buisness_name)
        return {"message": f"Store Name updated successfully for {store_uid}"}
    except Exception as e:
        raise CustomHTTPException(message=e)


#TODO: get rid of id from url instead use jwt token
@store_router.put("/store_type")
async def update_store_type(store_uid:str=  Form(...), type:str = Form(...)):
    try:
        store_service.update_store_buisness_type(store_uid=store_uid,type=type)
        return {"message": f"Store Type updated successfully for {store_uid}"}
    except Exception as e:
        raise CustomHTTPException(message=e)

#TODO: get rid of id from url instead use jwt token
@store_router.put("/store_address")
async def update_store_address(store_uid:str=  Form(...), address:str = Form(...), postal_code:str= Form(...)):
    try:
        store_service.update_store_buisness_address(store_uid=store_uid,address=address, postal_code=postal_code)
        return {"message": f"Store Address updated successfully for {store_uid}"}
    except Exception as e:
        raise CustomHTTPException(message=e)
    

    
#TODO: get rid of id from url instead use jwt token
@store_router.put("/store_gstno")
async def update_store_gstno(store_uid:str=  Form(...), gst_number:str = Form(...)):
    try:
        store_service.update_store_buisness_gst_number(store_uid=store_uid,gst_number=gst_number,)
        return {"message": f"Store gstno updated successfully for {store_uid}"}
    except Exception as e:
        raise CustomHTTPException(message=e)


@store_router.get("/store-users/{store_uid}")
async def users_assosiated_with_store(store_uid:str):
    try:
        users =store_service.get_privilege_record_by_store(store_uid)            
        return users
    except Exception as e:
        raise CustomHTTPException(message=e)
    

@store_router.get("/user-stores/{user_uid}/")
async def stores_assosiated_with_user(user_uid:str):
    try:
        stores =store_service.get_privilege_record_by_user(user_uid)            
        return stores
    except Exception as e:
        raise CustomHTTPException(message=e)
    

@store_router.post("/users")
async def add_user_to_store(user_uid:str = Form(...), 
                          store_uid:str = Form(...), 
                          role:str = Form(...)):
    try:
        store_service.create_privilege_record(user_uid,store_uid,role)            
        return {"message": f"User successfully added to store"}
    except Exception as e:
        raise CustomHTTPException(message=e)
    
@store_router.put("/users")
async def update_user_role_of_store(
                          uid:str = Form(...),
                          user_uid:str = Form(...), 
                          store_uid:str = Form(...), 
                          role:str = Form(...)):
    try:
        store_service.update_privilege_record(uid,user_uid,store_uid,role)            
        return {"message": f"User role information successfully modified"}
    except Exception as e:
        raise CustomHTTPException(message=e)
    

@store_router.delete("/users/{uid}")
async def delete_user_from_store(uid:str):
    try:
        store_service.delete_privilege_record(uid)            
        return {"message": f"User role information successfully modified"}
    except Exception as e:
        raise CustomHTTPException(message=e)
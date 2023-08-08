from fastapi import APIRouter
from fastapi import Depends,FastAPI, Form,Request,status, HTTPException,Response,File, UploadFile
from infrastructure.persistence.database.DatabaseSessionFactory import DatabaseSessionFactory
from application.unit_of_work import SqlAlchemyUnitOfWork
from application.fuelflow.service import FuelFlowService
from fastapi.responses import JSONResponse
from ..exception import CustomHTTPException
from .lob_sub_routers.unload_router import unload_router
from .lob_sub_routers.credit_router import credit_router
from .lob_sub_routers.registry_router import registry_router

sqlaclk_uow= SqlAlchemyUnitOfWork(DatabaseSessionFactory)
lob_router = APIRouter()
lob_service=FuelFlowService(sqlaclk_uow)


'''
GET /lob/all
GET /lob   
GET /lob/{uid}
POST /lob
DELETE /lob
PUT /lob 

GET /lob/activities
GET /lob/activities/{lob_uid}
POST /lob/activities/{lob_uid}
DELETE /lob/activities


GET /lob/roles
GET /lob/roles/{lob_uid}
POST /lob/roles/{uid}
DELETE /lob/roles/{uid}

GET /lob/privilege
GET /lob/privilege/{lob_uid}
POST /lob/privilege/{uid}
DELETE /lob/privilege/{uid}

GET /lob/rota
GET /lob/rota/{lob_uid}
POST /lob/rota/{lob_uid}
PUT /lob/rota/{uid}
DELETE /lob/rota/{uid}


GET /lob/pos
GET /lob/pos/{lob_uid}
POST /lob/pos/{lob_uid}
PUT /lob/pos/{lob_uid}
DELETE /lob/pos/{uid}

'''

@lob_router.get("/all")
async def list_all_lob():
    # Get user logic here
    try:

        lob=lob_service.get_lob()
        return lob
    
    except Exception as e:
        raise CustomHTTPException(message=e)



@lob_router.get("/by-user/{user_id}")
async def  list_lobs_associated_with_user_id(user_id:str):
    # Get user logic here
    try:
        lobs=lob_service.get_lob_by_user_id(user_id)
        return lobs
    except Exception as e:
        raise CustomHTTPException(message=e)


@lob_router.post("/")
async def create_new_store(
    buisness_name: str = Form(...), 
    type: str = Form(...), 
    address: str = Form(...), 
    postal_code: str = Form(...), 
    gst_number: str = Form(...), 
    user_uid: str = Form(...), 
):
    try:
        lob=lob_service.create_lob(buisness_name,type,address,postal_code,gst_number,user_uid)
        return {"message": f"Store created successfully for user ID {lob.uid}"}
    except Exception as e:
        raise CustomHTTPException(message=e)



@lob_router.delete("/{id}")
async def delete_user(id: str):
    try:
        users=lob_service.hard_delete_lob(uid=id)
        print("after return")
        return {"message": f"Lob {id} deleted successfully"}
    except Exception as e:
        raise CustomHTTPException(message=e)
    


@lob_router.get("/{lob_id}")
async def get_store_details(lob_id: str):
    # Get user logic here
    try:

        user=lob_service.get_lob_id(uid=lob_id)
        return user
    
    except Exception as e:
        raise CustomHTTPException(message=e)



#TODO: get rid of id from url instead use jwt token
@lob_router.put("/store_name")
async def update_store_name(lob_uid:str=  Form(...), buisness_name:str = Form(...)):
    try:
        lob_service.update_lob_buisness_name(lob_uid=lob_uid,buisness_name=buisness_name)
        return {"message": f"Store Name updated successfully for {lob_uid}"}
    except Exception as e:
        raise CustomHTTPException(message=e)


#TODO: get rid of id from url instead use jwt token
@lob_router.put("/store_type")
async def update_store_type(lob_uid:str=  Form(...), type:str = Form(...)):
    try:
        lob_service.update_lob_buisness_type(lob_uid=lob_uid,type=type)
        return {"message": f"Store Type updated successfully for {lob_uid}"}
    except Exception as e:
        raise CustomHTTPException(message=e)

#TODO: get rid of id from url instead use jwt token
@lob_router.put("/store_address")
async def update_lob_store_address(lob_uid:str=  Form(...), address:str = Form(...), postal_code:str= Form(...)):
    try:
        lob_service.update_lob_buisness_address(lob_uid=lob_uid,address=address, postal_code=postal_code)
        return {"message": f"Store Address updated successfully for {lob_uid}"}
    except Exception as e:
        raise CustomHTTPException(message=e)
    

    
#TODO: get rid of id from url instead use jwt token
@lob_router.put("/store_gstno")
async def update_lob_store_gstno(lob_uid:str=  Form(...), gst_number:str = Form(...)):
    try:
        lob_service.update_lob_buisness_gst_number(lob_uid=lob_uid,gst_number=gst_number,)
        return {"message": f"Store gstno updated successfully for {lob_uid}"}
    except Exception as e:
        raise CustomHTTPException(message=e)
    
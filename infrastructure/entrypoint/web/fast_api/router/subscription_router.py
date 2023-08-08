from fastapi import APIRouter
from fastapi import Depends,FastAPI, Form,Request,status, HTTPException,Response,File, UploadFile
from infrastructure.persistence.database.DatabaseSessionFactory import DatabaseSessionFactory
from application.unit_of_work import SqlAlchemyUnitOfWork
from application.subscription.service import SubscriptionService
from fastapi.responses import JSONResponse
from ..exception import CustomHTTPException
from typing import Optional, Literal

sqlaclk_uow= SqlAlchemyUnitOfWork(DatabaseSessionFactory)
subscription_router = APIRouter()
subscription_service=SubscriptionService(sqlaclk_uow)


@subscription_router.get("/plan")
async def list_plans():
    # Get user logic here
    try:
        plans=subscription_service.get_plans()
        return plans
    
    except Exception as e:
        raise CustomHTTPException(message=e)


@subscription_router.post("/plan")
async def create_plan(
    plan_type: str = Form(...), 
    plan_name: str = Form(...), 
    price: float = Form(...), 
    period: int = Form(...), 
    key: str = Form(...), 
    retention_limit: int = Form(...), 
    user_limit: int = Form(...), 
    status: str = Form(...), 
):
    try:

       plan=subscription_service.create_plan(plan_type,plan_name,price,period,key,retention_limit,user_limit,status)
       return plan
    except Exception as e:
        raise CustomHTTPException(message=e)


@subscription_router.put("/plan")
async def update_plan(    
    id: str=Form(...),
    plan_type: str = Form(...), 
    plan_name: str = Form(...), 
    price: float = Form(...), 
    period: int = Form(...), 
    key: str = Form(...), 
    retention_limit: int = Form(...), 
    user_limit: int = Form(...), 
    status: str = Form(...), 
):
    try:

       plan=subscription_service.update_plan(id,plan_type,plan_name,price,period,key,retention_limit,user_limit,status)
       return  {"message": f"Plan updated successfully"}
    except Exception as e:
        raise CustomHTTPException(message=e)



#TODO: get rid of id from url instead use jwt token
@subscription_router.delete("/plan/{id}")
async def delete_plan(id: str):
    try:
       plan=subscription_service.delete_plan(uid=id)
       return {"message": f"Plan deleted successfully - {id}"}
    except Exception as e:
        raise CustomHTTPException(message=e)


@subscription_router.get("/plan/{id}")
async def get_plan_details(id:str):
    try:

       plan=subscription_service.get_plan_by_id(id)
       return plan
    except Exception as e:
        raise CustomHTTPException(message=e)
    

@subscription_router.post("/subscribe")
async def subscribe(store_uid:str,initiated_user_uid:str,plan_id:str):
    try:
       
       plan=subscription_service.create_subscription(store_uid,initiated_user_uid,plan_id)
       return plan
    except Exception as e:
        raise CustomHTTPException(message=e)


@subscription_router.get("/{store_uid}")
async def get_subscription_for_store(store_uid:str, status: Optional[Literal["PENDING", "ACTIVE","EXPIRED", "NEEDS_RENEWAL"]] = None):
    try:
       sub=subscription_service.get_subscription(store_uid,status)
       return sub
    except Exception as e:
        raise CustomHTTPException(message=e)


@subscription_router.get("/")
async def get_subscription(status: Optional[Literal["PENDING", "ACTIVE","EXPIRED", "NEEDS_RENEWAL"]] = None):
    try:
       sub=subscription_service.get_subscription(None, status)
       return sub
    except Exception as e:
        raise CustomHTTPException(message=e)
    
@subscription_router.delete("/{store_uid}/{subscription_uid}")
async def delete_pending_subscription(store_uid:str, subscription_uid: str):
    try:
       sub=subscription_service.delete_pending_subscription(store_uid,subscription_uid)
       return sub
    except Exception as e:
        raise CustomHTTPException(message=e)


@subscription_router.post("/payment/order")
async def create_payment_order_for_subscription(subscription_uid:str):
    try:
       sub=subscription_service.get_subscription_id(subscription_uid)
       #return sub
       return None
    except Exception as e:
        raise CustomHTTPException(message=e)
    

@subscription_router.post("/payment/verify")
async def payment_verify():
    try:
       #
       #return sub
       return None
    except Exception as e:
        raise CustomHTTPException(message=e)



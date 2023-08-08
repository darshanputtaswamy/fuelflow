from fastapi import APIRouter
from fastapi import Depends,FastAPI, Form,Request,status, HTTPException,Response,File, UploadFile
from infrastructure.persistence.database.DatabaseSessionFactory import DatabaseSessionFactory
from application.unit_of_work import SqlAlchemyUnitOfWork
from application.fuelflow.service import FuelFlowService
from fastapi.responses import JSONResponse
from infrastructure.entrypoint.web.fast_api.exception import CustomHTTPException

sqlaclk_uow= SqlAlchemyUnitOfWork(DatabaseSessionFactory)
credit_router = APIRouter()
store_service=FuelFlowService(sqlaclk_uow)

def getverificationcode():
    return "newverificationcode"

def sendVerificationSME(code):
    print("new verification code is"+ code)



@credit_router.get("/")
async def list_users():
    # Get user logic here
    try:

        users=store_service.get_users()
        return users
    
    except Exception as e:
        raise CustomHTTPException(message=e)


@credit_router.post("/register")
async def create_user(
    username: str = Form(...), 
    phone: str = Form(...),
    email = Form(...),
    password:str = Form(...)
):
    try:

        id=store_service.add_user(username,phone,email,password)
        nv=getverificationcode()
        store_service.save_user_verification_code(user_id=id,verification_code=nv)
        sendVerificationSME(nv)
        return {"message": "User created successfully : " +str(id)}
    
    except Exception as e:
        raise CustomHTTPException(message=e)


@credit_router.get("/{id}/profile")
async def get_user(id: str):
    # Get user logic here
    try:

        user=store_service.get_user_by_id(uid=id)
        return user
    
    except Exception as e:
        raise CustomHTTPException(message=e)



#TODO: get rid of id from url instead use jwt token
@credit_router.put("/password")
async def change_password(id:str=  Form(...), new_password:str = Form(...)):
    try:
        users=store_service.update_user_password(user_id=id,password=new_password)
        return {"message": f"Password updated successfully for user ID {id}"}
    except Exception as e:
        raise CustomHTTPException(message=e)


@credit_router.put("/lock")
async def change_password(id:str=  Form(...), status=Form(...)):
    try:
        users=store_service.lock_user(user_id=id,status=status)
        return {"message": f"User {id}'s lock status is set to - {status} successfully"}
    except Exception as e:
        raise CustomHTTPException(message=e)

@credit_router.put("/username")
async def change_password(id:str=  Form(...), username=Form(...)):
    try:
        users=store_service.update_username(user_id=id,username=username)
        return {"message": f"User {id}'s username is set to - {username} successfully"}
    except Exception as e:
        raise CustomHTTPException(message=e)
    

@credit_router.put("/user_type")
async def change_password(id:str=  Form(...), type=Form(...)):
    try:
        users=store_service.update_user_type(user_id=id,value=type)
        return {"message": f"User {id}'s user_type is set to - {type} successfully"}
    except Exception as e:
        raise CustomHTTPException(message=e)
    
    

@credit_router.delete("/{id}")
async def delete_user(id: str):
    try:
        users=store_service.hard_delete_user(user_id=id)
        print("after return")
        return {"message": f"User {id} deleted successfully"}
    except Exception as e:
        raise CustomHTTPException(message=e)
    

#TODO: get rid of id from url instead use jwt token
@credit_router.post("/verify")
async def verify_user(id:str=  Form(...), verification_code:str = Form(...)):
    # Verify user logic here
    try: 
        saved_verification_code = store_service.get_user_verification_code(user_id=id)
        if saved_verification_code == verification_code:
            store_service.is_verified(user_id=id)
            return {"message": "User verified successfully"}
        else:
            raise "verification failed" 
    except Exception as e:
        raise CustomHTTPException(message=e)
    

#TODO: get rid of id from url instead use jwt token
@credit_router.get("/resend-verification/{id}")
async def resend_verification(id: str):
    # Verify user logic here
    try: 
        nv=getverificationcode()
        store_service.save_user_verification_code(user_id=id,verification_code=nv)
        sendVerificationSME(nv)
        return {"message": "Verification email sent successfully"}
    except Exception as e:
        raise CustomHTTPException(message=e)

    
'''
# Additional Endpoints

@credit_router.post("/users/login")
async def user_login(credentials: UserCredentials):
    # User login logic here
    return {"access_token": "jwt_token"}


@credit_router.post("/refresh", response_model=Token)
async def refresh_token(token_refresh: TokenRefresh, authorize: AuthJWT = Depends()):
    authorize.jwt_refresh_token_required()

    # Access token refresh is valid, generate new access token
    current_user = authorize.get_jwt_subject()
    new_access_token = authorize.create_access_token(subject=current_user)

    return {"access_token": new_access_token, "refresh_token": token_refresh.refresh_token}

@credit_router.post("/users/logout")
async def user_logout():
    # User logout logic here
    return {"message": "User logged out successfully"}

'''
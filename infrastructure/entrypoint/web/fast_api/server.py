import datetime
from fastapi import Depends,FastAPI, Form,Request,status, HTTPException,Response,File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.gzip import GZipMiddleware
import configparser
import json
import sys
import os
from fastapi.middleware.cors import CORSMiddleware
from .auth import AuthHandler 
import os 
import pandas as pd
from .router.user_router import user_router
from .router.subscription_router import subscription_router

from .exception import CustomHTTPException

app = FastAPI()
auth_handler = AuthHandler()

origins = ["*"]
app.add_middleware(GZipMiddleware, minimum_size=1000)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(CustomHTTPException)
async def custom_exception_handler(request: Request, exc: CustomHTTPException):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, 
        content={"message": f"{exc.message}" })



class CustomHTTPException(Exception):
    def __init__(self, message: str):
        self.message = message

@app.exception_handler(CustomHTTPException)
async def custom_exception_handler(request: Request, exc: CustomHTTPException):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, 
        content={"message": f"{exc.message}" })

app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(subscription_router, prefix="/subscription", tags=["Subscription"])



'''




import datetime
from fastapi import Depends,FastAPI, Form,Request,status, HTTPException,Response,File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.gzip import GZipMiddleware
import configparser
import json
from application.FuelFlowApplication import DARTApplication
from application.unit_of_work import SqlAlchemyUnitOfWork
from infrastructure.persistence.database.DatabaseSessionFactory import DatabaseSessionFactory
import requests_oauthlib
import sys
import os
from fastapi.middleware.cors import CORSMiddleware
from .auth import AuthHandler 
import os 
from pathlib import Path
Path.cwd()
import pandas as pd

sqlaclk_uow= SqlAlchemyUnitOfWork(DatabaseSessionFactory)
DARTApp=DARTApplication(sqlaclk_uow,Path.cwd().joinpath('infrastructure').joinpath('persistence').joinpath('appdata'))
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

config = configparser.ConfigParser()
app = FastAPI()
auth_handler = AuthHandler()

origins = ["*"]
app.add_middleware(GZipMiddleware, minimum_size=1000)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class CustomHTTPException(Exception):
    def __init__(self, message: str):
        self.message = message

@app.exception_handler(CustomHTTPException)
async def custom_exception_handler(request: Request, exc: CustomHTTPException):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, 
        content={"message": f"{exc.message}" })

@app.get("/auth/v1/sso/login")
async def handleSSOLoginCallback(authcode, request: Request):
    try:
        simplelogin = requests_oauthlib.OAuth2Session(CLIENT_ID)
        simplelogin.fetch_token(ACCESS_TOKEN_URL, client_secret=CLIENT_SECRET, code=authcode)
        user_info = simplelogin.get(USERINFO_URL).json()
        token = auth_handler.encode_token(user_info)
        return token
    except Exception as e:
        raise CustomHTTPException(message=e)
    

@app.post("/rca")
async def createRCA(
    name: str = Form(...), 
    description: str = Form(...),
    primary_key_column = Form(...),
    default_start_date_column:str = Form(...),
    default_end_date_column:str = Form(...),
    column_categorization:str = Form(...),
    default_categorical_column: str = Form(...),
    default_numerical_column: str = Form(...),
    retention_days:int = Form(...), 
    file: UploadFile  = File(...),
    jwt=Depends(auth_handler.auth_wrapper)):
    try:
        rca={}
        rca['name']=name
        rca['description']=description
        rca['owner']=jwt['payload']['email']
        rca['primary_key_column']=primary_key_column
        rca['default_categorical_column']=default_categorical_column
        rca['default_numerical_column']=default_numerical_column
        rca['default_start_date_column']=default_start_date_column
        rca['default_end_date_column']=default_end_date_column
        rca['column_categorization']=column_categorization
        rca['created_date']=datetime.datetime.now()
        rca['retention_days']=retention_days
        rca['status']='WIP'
        rca['filename']=file.filename
        result=DARTApp.add_rca(rca,file)
        return result
    except Exception as e:
        raise CustomHTTPException(message=e)
    return {"name": name, "email": description, "file": file}

@app.get("/rca")
async def getRCAList(request: Request,jwt=Depends(auth_handler.auth_wrapper)):
    try:
        print(jwt['payload']['email'])
        result=DARTApp.get_rca_metadata_list(user_id=jwt['payload']['email'])
        print(result)
        return result
    except Exception as e:
        raise CustomHTTPException(message=e)
    
@app.get("/rca/{id}")
async def getRCADetails(id,jwt=Depends(auth_handler.auth_wrapper)):
    try:
        print(jwt['payload']['email'])
        result=DARTApp.get_rca_metadata(id,user_id=jwt['payload']['email'])
        return result[0]
    except Exception as e:
        raise CustomHTTPException(message=e)
    

@app.put("/rca/{id}")
async def updateRCA(id,
                    description: str = Form(...),
                    default_start_date_column:str = Form(...),
                    primary_key_column = Form(...),
                    default_end_date_column:str = Form(...),
                    column_categorization:str = Form(...),
                    default_categorical_column: str = Form(...),
                    default_numerical_column: str = Form(...),
                    retention_days:int = Form(...),
                    status:str = Form(...),
                    jwt=Depends(auth_handler.auth_wrapper)):
    try:
        rca={}
        rca['id']=id
        rca['description']=description
        rca['primary_key_column']=primary_key_column
        rca['default_categorical_column']=default_categorical_column
        rca['default_numerical_column']=default_numerical_column
        rca['default_start_date_column']=default_start_date_column
        rca['default_end_date_column']=default_end_date_column
        rca['column_categorization']=column_categorization
        rca['retention_days']=retention_days
        rca['status']=status
        print('=======================')
        print(rca)
        DARTApp.update_rca_metadata(rca,user_id=jwt['payload']['email'])
        return "updated successfully"
    except Exception as e:
        raise CustomHTTPException(message=e)
    
    
@app.get("/rcadata/{id}")
async def getRCADdata(id,jwt=Depends(auth_handler.auth_wrapper)):
    try:
        print(jwt['payload']['email'])
        result=DARTApp.get_rca_data(id=id)
        return result.to_json()
    except Exception as e:
        raise CustomHTTPException(message=e)



@app.delete("/rca/{id}")
async def getRCADdata(id,jwt=Depends(auth_handler.auth_wrapper)):
    try:
        result=DARTApp.delete_rca(rca_id=id,user_id=jwt['payload']['email'])
        return result
    except Exception as e:
        raise CustomHTTPException(message=e)
    

@app.post("/rca/permission/{rca_id}")
async def addUserToRCA(rca_id, userlist: str = Form(...),jwt=Depends(auth_handler.auth_wrapper)):
    res=[]
    try:
        for user in userlist.split(","):
            id=DARTApp.add_user(rca_id=rca_id,shared_user=user,user_id=jwt['payload']['email'])
            res.append({'id':id,'rca_id':rca_id,'user_id':user})
        return res
    except Exception as e:
        raise CustomHTTPException(message=e)
    

@app.delete("/rca/permission/{rca_id}/{id}")
async def addUserToRCA(rca_id, id,jwt=Depends(auth_handler.auth_wrapper)):
    res=[]
    try:
        id=DARTApp.delete_user(rca_id=rca_id, id=id,user_id=jwt['payload']['email'])
        return res
    except Exception as e:
        raise CustomHTTPException(message=e)

@app.post("/rca/comment/{rca_id}")
async def addComment(rca_id, analyser: str= Form(...) ,comment: str= Form(...) ,owner: str= Form(...),type: str= Form(...) ,jwt=Depends(auth_handler.auth_wrapper)):
    try:
        id,created_date=DARTApp.add_comment(rca_id=rca_id, analyser=analyser,comment=comment,type=type, owner=jwt['payload']['email'])
        return {'id':id,'rca_id':rca_id, 'analyser':analyser,'comment':comment,'type':type, 'owner':jwt['payload']['email'],'created_date':created_date}
    except Exception as e:
        raise CustomHTTPException(message=e)
    
@app.delete("/rca/comment/{rca_id}/{id}")
async def deleteComment(rca_id,id, jwt=Depends(auth_handler.auth_wrapper)):
    try:
        DARTApp.delete_comment(rca_id=rca_id,id=id,user_id=jwt['payload']['email'])
        return "Deleted Successfully"
    except Exception as e:
        raise CustomHTTPException(message=e)
    

@app.get("/rca/distinct_values/{rca_id}/{columnlist}")
async def getDistinctValues(rca_id, columnlist ,jwt=Depends(auth_handler.auth_wrapper)):
    res={}
    try:
        result=DARTApp.get_rca_data(id=rca_id)
        result = result.fillna('')
        for col in columnlist.split(','):
            res[col]=result[col].unique().tolist()
            res[col].insert(0,'ALL')
        return res
    except Exception as e:
        raise CustomHTTPException(message=e)
    
@app.get("/rca/minmaxdate/{rca_id}/{date_column}")
async def getDistinctValues(rca_id,date_column,jwt=Depends(auth_handler.auth_wrapper)):
    res={}
    try:
        result=DARTApp.get_rca_data(id=rca_id)
        
        if date_column not in result.columns:
            raise CustomHTTPException(message='Invalid request, field not found')
        result[date_column]=pd.to_datetime(result[date_column])
        return {'mindate':min(result[date_column]),'maxdate':max(result[date_column])}
    except Exception as e:
        raise CustomHTTPException(message=e)
    

@app.post("/rca/volumn_analysis/{rca_id}")
async def volumnAnalysis(rca_id, config: str= Form(...) ,jwt=Depends(auth_handler.auth_wrapper)):
    res={}
    try:
        print(config)
        result=DARTApp.get_rca_data(id=rca_id)
        result = result.fillna('')
        config = json.loads(config)
        return volume_analysis(config,result)
    except Exception as e:
        raise CustomHTTPException(message=e)
    
@app.post("/rca/histogram_analysis/{rca_id}")
async def histogramAnalysis(rca_id, config: str= Form(...) ,jwt=Depends(auth_handler.auth_wrapper)):
    res={}
    try:
        result=DARTApp.get_rca_data(id=rca_id)
        result = result.fillna('')
        config = json.loads(config)
        return histogram_analysis(config,result)
    except Exception as e:
        raise CustomHTTPException(message=e)
    

@app.post("/rca/timeline_analysis/{rca_id}")
async def timelineAnalysis(rca_id, config: str= Form(...) ,jwt=Depends(auth_handler.auth_wrapper)):
    res={}
    try:
        print(config)
        result=DARTApp.get_rca_data(id=rca_id)
        result = result.fillna('')
        config = json.loads(config)
        res = timeline_analysis(config,result)
        print("===============")
        return res
    except Exception as e:
        raise CustomHTTPException(message=e)
 '''
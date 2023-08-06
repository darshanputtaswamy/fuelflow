from warnings import catch_warnings
#from application.lob.lob_service import LobService
#from application.subscription.subscription_service import SubscriptionService
from application.user.user_service import UserService
import datetime
import uuid
import shutil
import pandas as pd
import os


class FuelFlowApplication(UserService): #,SubscriptionService,LobService
    def __init__(self,uow,base_dir):
        super().__init__(uow,base_dir)
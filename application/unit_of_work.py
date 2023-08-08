# pylint: disable=attribute-defined-outside-init
from __future__ import annotations
import abc
from sqlalchemy import create_engine

from infrastructure.repository.core.app_users_sa_repo import AppUsersSQLAlchemyRepository
from infrastructure.repository.fuelflow.store_sa_repo import StoreSQLAlchemyRepository
from infrastructure.repository.fuelflow.store_sa_repo import StoreActivitiesSQLAlchemyRepository
from infrastructure.repository.fuelflow.store_sa_repo import StoreRolesSQLAlchemyRepository
from infrastructure.repository.fuelflow.store_sa_repo import StoreUserPrivilegeSQLAlchemyRepository
from infrastructure.repository.fuelflow.store_sa_repo import StoreRotaSQLAlchemyRepository
from infrastructure.repository.fuelflow.store_sa_repo import POSSQLAlchemyRepository
from infrastructure.repository.core.subscription_sa_repo import PlansSQLAlchemyRepository
from infrastructure.repository.core.subscription_sa_repo import SubscriptionSQLAlchemyRepository
from infrastructure.repository.core.subscription_sa_repo import SubscriptionPaymentOrderSQLAlchemyRepository
from infrastructure.repository.fuelflow.credit_sa_repo import VechiclesSQLAlchemyRepository
from infrastructure.repository.fuelflow.credit_sa_repo import OrderSQLAlchemyRepository
from infrastructure.repository.fuelflow.credit_sa_repo import OrderLineItemSQLAlchemyRepository
from infrastructure.repository.fuelflow.registry_sa_repo import FuelRegistrySQLAlchemyRepository
from infrastructure.repository.fuelflow.unload_sa_repo import FuelDipReaderSQLAlchemyRepository
from infrastructure.repository.fuelflow.unload_sa_repo import UnloaderSQLAlchemyRepository
from infrastructure.repository.base import AbstractRepository

class AbstractUnitOfWork(abc.ABC):
    user: AbstractRepository
    store: AbstractRepository
    store_activities: AbstractRepository
    store_roles: AbstractRepository
    store_user_privileges: AbstractRepository
    store_rota: AbstractRepository
    store_pos: AbstractRepository
    store_vehiceles: AbstractRepository
    store_credit_order: AbstractRepository
    store_credit_orderlineItems: AbstractRepository
    store_registry: AbstractRepository
    fueldip_reader: AbstractRepository
    fuel_unloader: AbstractRepository
    plans: AbstractRepository
    subscription: AbstractRepository
    PaymentOrder: AbstractRepository
    

    def __enter__(self) -> AbstractUnitOfWork:
        return self

    def __exit__(self, *args):
        self.rollback()

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory):
        self.session_factory = session_factory()
        self.rca = None
        self.comments = None
        self.permissions = None
        self.user: None
        self.store: None
        self.store_activities: None
        self.store_roles: None
        self.store_user_privileges: None
        self.store_rota: None
        self.store_pos: None
        self.store_vehiceles: None
        self.store_credit_order: None
        self.store_credit_orderlineItems: None
        self.store_registry: None
        self.fueldip_reader: None
        self.fuel_unloader: None
        self.plans: None
        self.subscription: None
        self.payment:None

    def __enter__(self):
        self.session = self.session_factory.create_session()  
        self.user= AppUsersSQLAlchemyRepository(self.session)
        self.store= StoreSQLAlchemyRepository(self.session)
        self.store_activities= StoreActivitiesSQLAlchemyRepository(self.session)
        self.store_roles= StoreRolesSQLAlchemyRepository(self.session)
        self.store_user_privileges= StoreUserPrivilegeSQLAlchemyRepository(self.session)
        self.store_rota= StoreRotaSQLAlchemyRepository(self.session)
        self.store_pos= POSSQLAlchemyRepository(self.session)
        self.store_vehiceles= VechiclesSQLAlchemyRepository(self.session)
        self.store_credit_order= OrderSQLAlchemyRepository(self.session)
        self.store_credit_orderlineItems= OrderLineItemSQLAlchemyRepository(self.session)
        self.store_registry= FuelRegistrySQLAlchemyRepository(self.session)
        self.fueldip_reader= FuelDipReaderSQLAlchemyRepository(self.session)
        self.fuel_unloader= UnloaderSQLAlchemyRepository(self.session)
        self.plans= PlansSQLAlchemyRepository(self.session)
        self.subscription= SubscriptionSQLAlchemyRepository(self.session)
        self.payment= SubscriptionPaymentOrderSQLAlchemyRepository(self.session)

        return super().__enter__()

    def __exit__(self,*arg,**kwargs):
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

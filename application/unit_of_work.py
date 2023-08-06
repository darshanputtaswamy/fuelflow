# pylint: disable=attribute-defined-outside-init
from __future__ import annotations
import abc
from sqlalchemy import create_engine

from infrastructure.repository.core.app_users_sa_repo import AppUsersSQLAlchemyRepository
from infrastructure.repository.core.lob_sa_repo import LOBSQLAlchemyRepository
from infrastructure.repository.core.lob_sa_repo import LOBActivitiesSQLAlchemyRepository
from infrastructure.repository.core.lob_sa_repo import LOBRolesSQLAlchemyRepository
from infrastructure.repository.core.lob_sa_repo import LOBUserPrivilegeSQLAlchemyRepository
from infrastructure.repository.core.lob_sa_repo import LOBRotaSQLAlchemyRepository
from infrastructure.repository.core.lob_sa_repo import POSSQLAlchemyRepository
from infrastructure.repository.core.subscription_sa_repo import PlansSQLAlchemyRepository
from infrastructure.repository.core.subscription_sa_repo import SubscriptionOrdersSQLAlchemyRepository
from infrastructure.repository.fuel.credit_sa_repo import VechiclesSQLAlchemyRepository
from infrastructure.repository.fuel.credit_sa_repo import OrderSQLAlchemyRepository
from infrastructure.repository.fuel.credit_sa_repo import OrderLineItemSQLAlchemyRepository
from infrastructure.repository.fuel.registry_sa_repo import FuelRegistrySQLAlchemyRepository
from infrastructure.repository.fuel.unload_sa_repo import FuelDipReaderSQLAlchemyRepository
from infrastructure.repository.fuel.unload_sa_repo import UnloaderSQLAlchemyRepository
from infrastructure.repository.base import AbstractRepository

class AbstractUnitOfWork(abc.ABC):
    user: AbstractRepository
    lob: AbstractRepository
    lob_activities: AbstractRepository
    lob_roles: AbstractRepository
    lob_user_privileges: AbstractRepository
    lob_rota: AbstractRepository
    lob_pos: AbstractRepository
    lob_vehiceles: AbstractRepository
    lob_credit_order: AbstractRepository
    lob_credit_orderlineItems: AbstractRepository
    lob_registry: AbstractRepository
    fueldip_reader: AbstractRepository
    fuel_unloader: AbstractRepository
    plans: AbstractRepository
    subscription: AbstractRepository
    

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
        self.lob: None
        self.lob_activities: None
        self.lob_roles: None
        self.lob_user_privileges: None
        self.lob_rota: None
        self.lob_pos: None
        self.lob_vehiceles: None
        self.lob_credit_order: None
        self.lob_credit_orderlineItems: None
        self.lob_registry: None
        self.fueldip_reader: None
        self.fuel_unloader: None
        self.plans: None
        self.subscription: None

    def __enter__(self):
        self.session = self.session_factory.create_session()  
        self.user= AppUsersSQLAlchemyRepository(self.session)
        self.lob= LOBSQLAlchemyRepository(self.session)
        self.lob_activities= LOBActivitiesSQLAlchemyRepository(self.session)
        self.lob_roles= LOBRolesSQLAlchemyRepository(self.session)
        self.lob_user_privileges= LOBUserPrivilegeSQLAlchemyRepository(self.session)
        self.lob_rota= LOBRotaSQLAlchemyRepository(self.session)
        self.lob_pos= POSSQLAlchemyRepository(self.session)
        self.lob_vehiceles= VechiclesSQLAlchemyRepository(self.session)
        self.lob_credit_order= OrderSQLAlchemyRepository(self.session)
        self.lob_credit_orderlineItems= OrderLineItemSQLAlchemyRepository(self.session)
        self.lob_registry= FuelRegistrySQLAlchemyRepository(self.session)
        self.fueldip_reader= FuelDipReaderSQLAlchemyRepository(self.session)
        self.fuel_unloader= UnloaderSQLAlchemyRepository(self.session)
        self.plans= PlansSQLAlchemyRepository(self.session)
        self.subscription= SubscriptionOrdersSQLAlchemyRepository(self.session)

        return super().__enter__()

    def __exit__(self,*arg,**kwargs):
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

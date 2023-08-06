from sqlalchemy import Table, MetaData, Column, Integer, String, Date, ForeignKey,Text,DateTime
from sqlalchemy.ext.declarative import declarative_base
from typing import List
from typing import Optional
from sqlalchemy import String
from sqlalchemy import event, inspect
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped,Mapper
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import mapper, relationship
from datetime import datetime

class Base(DeclarativeBase):
    pass

metadata = Base.metadata


class AppUsersORM(Base):
    __tablename__ = "app_users"
    uid: Mapped[str] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(60))
    phone: Mapped[str]
    email: Mapped[str] 
    password:Mapped[str]
    user_type: Mapped[str] 
    is_locked: Mapped[str] 
    is_verified: Mapped[str] 
    created_date: Mapped[datetime] 
    is_deleted: Mapped[str] 
    user_roles: Mapped[Optional[List["LOBUserPrivilegeORM"]]] = relationship(back_populates="user_details", cascade="all, delete-orphan")    
    def __repr__(self) -> str:
      return f"AppUsers(id={self.uid!r}, username={self.username!r}, phone={self.phone!r})"
    
class AppUserVerificationORM(Base):
    __tablename__ = "app_users_verification"
    uid: Mapped[str] = mapped_column(primary_key=True)
    user_uid: Mapped[str] = mapped_column(ForeignKey("app_users.uid"))
    verification_code: Mapped[str]

    
class PlansORM(Base):
   __tablename__ = 'plans'
   uid: Mapped[str] = mapped_column(primary_key=True)
   plan_type:Mapped[str]
   plan_name:Mapped[str]
   price:Mapped[float]
   period:Mapped[int]
   key:Mapped[str]
   retention_limit:Mapped[int]
   user_limit:Mapped[int]
   status:Mapped[str]
   created_date: Mapped[datetime] 
   updated_date: Mapped[Optional[datetime]] 

   def __repr__(self) -> str:
      return f"Plans(id={self.uid!r}, plan_name={self.plan_name!r})"

class SubscriptionOrdersORM(Base):
   __tablename__ = 'subscription_orders'
   uid: Mapped[str] = mapped_column(primary_key=True)
   lob_uid: Mapped[str] =  mapped_column(ForeignKey("lob.uid"))
   initiated_user_uid:Mapped[str] =  mapped_column(ForeignKey("app_users.uid"))
   plan_id:Mapped[str] = mapped_column(ForeignKey("plans.uid"))
   paid_amount:Mapped[float] 
   receipt_id:Mapped[str]
   status:Mapped[str]
   payment_id:Mapped[str]
   order_id:Mapped[str]
   signature:Mapped[str]
   created_date: Mapped[datetime] 
   updated_date: Mapped[Optional[datetime]] 
   plan_details:Mapped["PlansORM"] = relationship("PlansORM")
   lob_details:Mapped["LOBORM"] = relationship(back_populates="subscription_history")
   
   def __repr__(self) -> str:
      return f"SubscriptionOrders(lob_uid={self.lob_uid!r}, initiated_user={self.initiated_user!r}, created_date={self.created_date}, paid_amount={self.paid_amount}, status={self.status})"
   


class LOBORM(Base):
   __tablename__ = 'lob'
   uid: Mapped[str] = mapped_column(primary_key=True)
   buisness_name: Mapped[str]
   type:Mapped[str]
   address: Mapped[str]
   postal_code: Mapped[str]
   gst_number: Mapped[str] 
   subscription_status:Mapped[str]
   is_deleted:Mapped[str]
   created_date: Mapped[datetime] 
   updated_date: Mapped[Optional[datetime]] 

   lob_user_roles: Mapped[Optional[List["LOBUserPrivilegeORM"]]] = relationship(
        back_populates="lob_details", cascade="all, delete-orphan")
   
   subscription_history:Mapped[Optional[list["SubscriptionOrdersORM"]]] = relationship(
        back_populates="lob_details", cascade="all, delete-orphan")
   
   pos_list:Mapped[Optional[List["POSORM"]]]  =  relationship(back_populates="lob_details", cascade="all, delete-orphan") 

   employee_rota:Mapped[Optional[List["LOBRotaORM"]]] = relationship(back_populates="lob_details",  cascade="all, delete-orphan")


   lob_credit_vehicles:Mapped[Optional[List["LOBCreditVehiclesORM"]]] =  relationship(back_populates="lob_details", cascade="all, delete-orphan") 

   def __repr__(self) -> str:
      return f"LOB(uid={self.uid!r}, buisness_name={self.buisness_name!r}, gst_number={self.gst_number!r})"
   

class LOBUserPrivilegeORM(Base):
    __tablename__ = "lob_user_roles"
    uid: Mapped[str] = mapped_column(primary_key=True)
    user_uid: Mapped[str] = mapped_column(ForeignKey("app_users.uid"))
    lob_uid: Mapped[str] = mapped_column(ForeignKey("lob.uid"))
    role:Mapped[str]
    created_date: Mapped[datetime] 
    updated_date: Mapped[Optional[datetime]] 
    lob_details: Mapped[LOBORM] = relationship(back_populates="lob_user_roles")
    user_details: Mapped[AppUsersORM] = relationship(back_populates="user_roles") 
    
    def __repr__(self) -> str:
      return f"LOBUserPrivilegeORM(id={self.uid!r}, user_uid={self.user_uid!r}, lob_uid={self.lob_uid!r}): role={self.role}"


class POSORM(Base):
   __tablename__ = 'pos'
   uid: Mapped[str] = mapped_column(primary_key=True)
   lob_uid: Mapped[str] = mapped_column(ForeignKey("lob.uid"))
   pos_name:Mapped[str]
   pos_type:Mapped[str]
   pos_contact_uid:Mapped[str] = mapped_column(ForeignKey("app_users.uid"))
   created_date: Mapped[datetime] 
   updated_date: Mapped[Optional[datetime]] 
   lob_details:Mapped[LOBORM] =  relationship(back_populates="pos_list")   
   fuel_registry:Mapped[Optional[List["FuelRegistryORM"]]]= relationship(back_populates="pos_details")   

   
   def __repr__(self) -> str:
      return f"LOBPOS(uid={self.uid!r}, lob_uid={self.lob_uid},pos_name={self.pos_name!r}, pos_type={self.pos_type!r})"
   
class LOBActivitiesORM(Base):
   __tablename__ = 'lob_employee_activities'
   uid: Mapped[str] = mapped_column(primary_key=True)
   lob_uid: Mapped[str] = mapped_column(ForeignKey("lob.uid"))
   activity_type: Mapped[str]
   def __repr__(self) -> str:
      return f"LOBActivitiesORM(uid={self.uid!r}, lob_uid={self.lob_uid},activity_type={self.activity_type!r}"
   


class LOBRolesORM(Base):
   __tablename__ = 'lob_employee_roles'
   uid: Mapped[str] = mapped_column(primary_key=True)
   lob_uid: Mapped[str] = mapped_column(ForeignKey("lob.uid"))
   roles: Mapped[str]
   def __repr__(self) -> str:
      return f"LOBRolesORM(uid={self.uid!r}, lob_uid={self.lob_uid},roles={self.roles!r}"

class LOBRotaORM(Base):
   __tablename__ = 'lob_employee_rota'
   uid: Mapped[str] = mapped_column(primary_key=True)
   lob_uid: Mapped[str] = mapped_column(ForeignKey("lob.uid"))
   user_uid: Mapped[str] = mapped_column(ForeignKey("app_users.uid"))
   from_date:Mapped[datetime]
   till_date:Mapped[datetime]
   role_uid: Mapped[str] = mapped_column(ForeignKey("lob_employee_roles.uid"))
   activity_uid: Mapped[str] = mapped_column(ForeignKey("lob_employee_activities.uid"))
   approval_status:Mapped[str]
   lob_details:Mapped["LOBORM"] = relationship(back_populates="employee_rota")   
   registry_record:Mapped[Optional["FuelRegistryORM"]] = relationship(back_populates="rota_details")

   def __repr__(self) -> str:
      return f"LOBEmployeeActivities(uid={self.uid!r}, lob_uid={self.lob_uid}, user_uid={self.user_uid}, from_date={self.from_date},till_date={self.till_date},role={self.role_uid},activity={self.activity_uid},approval_status={self.approval_status}"


class FuelRegistryORM(Base):
    __tablename__ = 'lob_fuel_registry'
    uid: Mapped[str] = mapped_column(primary_key=True)
    lob_uid: Mapped[str] = mapped_column(ForeignKey("lob.uid"))
    pos_uid: Mapped[str] = mapped_column(ForeignKey("pos.uid"))
    rota_uid:Mapped[str] =  mapped_column(ForeignKey("lob_employee_rota.uid"), nullable=True)
    previous_uid:Mapped[Optional[str]] 
    status:Mapped[str]
    closing_reading:Mapped[float]
    opening_reading:Mapped[float]
    total_sales:Mapped[float]
    rate:Mapped[float]
    total:Mapped[float]
    cash_amount_received:Mapped[float]
    card_amount_received:Mapped[float]
    upi_amount_received:Mapped[float]
    expenditure:Mapped[float]
    credits:Mapped[float]
    balance:Mapped[float]
    rota_details:Mapped[Optional["LOBRotaORM"]] = relationship(back_populates="registry_record")
    pos_details:Mapped[Optional["POSORM"]] = relationship(back_populates="fuel_registry")       
    def __repr__(self) -> str:
      return f"FuelRegistry(uid={self.uid!r}"


class LOBCreditVehiclesORM(Base):
  __tablename__ = 'lob_credit_vehicles'
  uid: Mapped[str] = mapped_column(primary_key=True)
  lob_uid: Mapped[str] = mapped_column(ForeignKey("lob.uid"))
  user_uid: Mapped[str] = mapped_column(ForeignKey("app_users.uid"))
  vehicle_num:Mapped[str]
  status:Mapped[str]
  lob_details:Mapped["LOBORM"] = relationship(back_populates="lob_credit_vehicles")  

  def __repr__(self) -> str:
      return f"CreditorsVehicals(uid={self.uid!r}, lob_uid={self.lob_uid},vehical_num={self.vehical_num},status={self.status})"


class LOBCreditOrdersORM(Base):
    __tablename__ = 'lob_credit_order'
    uid:Mapped[str] = mapped_column(primary_key=True)
    pos_uid: Mapped[str] = mapped_column(ForeignKey("pos.uid"))
    lob_uid: Mapped[str] = mapped_column(ForeignKey("lob.uid"))
    rota_uid:Mapped[str] =  mapped_column(ForeignKey("lob_employee_rota.uid"))
    user_uid: Mapped[str] = mapped_column(ForeignKey("app_users.uid"))
    total_amount:Mapped[float]
    type:Mapped[str]  #check if it is possible to use one of two values 
    created_date: Mapped[datetime] 
    updated_date: Mapped[Optional[datetime]]
    payment_mode:Mapped[Optional[str]]

   
class LOBCreditOrderLineItemsORM(Base):
    __tablename__ = 'lob_credit_order_line_items'
    uid:Mapped[str] = mapped_column(primary_key=True)
    order_id:Mapped[str]= mapped_column(ForeignKey("lob_credit_order.uid"))
    vehicle_id:Mapped[str]= mapped_column(ForeignKey("lob_credit_vehicles.uid"))
    liters:Mapped[float]
    rate:Mapped[float]
    amount:Mapped[float]


class FuelDipReaderORM(Base):
    __tablename__ = 'lob_dip_readings'
    uid:Mapped[str] = mapped_column(primary_key=True)
    lob_uid: Mapped[str] = mapped_column(ForeignKey("lob.uid"))
    fuel_tank:Mapped[str]
    dip_number:Mapped[float]
    liters:Mapped[float]

class FuelUnloadingBookORM(Base):
    __tablename__ = 'lob_fuel_unloading_book'
    uid:Mapped[str] = mapped_column(primary_key=True)
    lob_uid: Mapped[str] = mapped_column(ForeignKey("lob.uid"))
    unload_date:Mapped[datetime]
    fuel_tank:Mapped[str]
    vehicle_number:Mapped[str]
    depo_name:Mapped[str]
    sample_box:Mapped[str]
    before_unload_dip_reading:Mapped[Optional[float]]
    before_unload_liters:Mapped[Optional[float]]
    after_unload_dip_reading:Mapped[Optional[float]]
    after_unload_liters:Mapped[Optional[float]]
    sales:Mapped[Optional[float]]
    bill_density:Mapped[Optional[float]]
    check_density:Mapped[Optional[float]]


@event.listens_for(Mapper, 'init')
def received_init(target, args, kwargs):
    """Allow initializing nested relationships with dict only"""
    print(kwargs)
    if 'uid' in kwargs and type(kwargs['uid']) != 'string':
        kwargs['uid']=str(kwargs['uid'])

    if 'pos_uid' in kwargs and type(kwargs['pos_uid']) != 'string':
        kwargs['pos_uid']=str(kwargs['pos_uid'])

    if 'rota_uid' in kwargs and type(kwargs['rota_uid']) != 'string':
        kwargs['rota_uid']=str(kwargs['rota_uid'])

    if 'previous_uid' in kwargs and type(kwargs['previous_uid']) != 'string':
        kwargs['previous_uid']=str(kwargs['previous_uid'])

    if 'lob_uid' in kwargs and type(kwargs['lob_uid']) != 'string':
        kwargs['lob_uid']=str(kwargs['lob_uid'])

    if 'user_uid' in kwargs and type(kwargs['user_uid']) != 'string':
        kwargs['user_uid']=str(kwargs['user_uid'])

    if 'initiated_user_uid' in kwargs and type(kwargs['initiated_user_uid']) != 'string':
        kwargs['initiated_user_uid']=str(kwargs['initiated_user_uid'])
    
    if 'pos_contact_uid' in kwargs and type(kwargs['pos_contact_uid']) != 'string':
        kwargs['pos_contact_uid']=str(kwargs['pos_contact_uid'])


    if 'vehicle_id' in kwargs and type(kwargs['vehicle_id']) != 'string':
        kwargs['vehicle_id']=str(kwargs['vehicle_id'])
    
    if 'order_id' in kwargs and type(kwargs['order_id']) != 'string':
        kwargs['order_id']=str(kwargs['order_id'])

    if 'plan_id' in kwargs and type(kwargs['plan_id']) != 'string':
        kwargs['plan_id']=str(kwargs['plan_id'])


    if 'role_uid' in kwargs and type(kwargs['role_uid']) != 'string':
        kwargs['role_uid']=str(kwargs['role_uid'])

    if 'activity_uid' in kwargs and type(kwargs['activity_uid']) != 'string':
        kwargs['activity_uid']=str(kwargs['activity_uid'])
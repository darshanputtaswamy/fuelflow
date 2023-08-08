from domain.core.app_users import AppUsers, AppUserVerification
from domain.fuelflow.store import Store,StoreActivities,StoreRoles,StoreRota,StoreUserPrivilege,POS
from domain.core.subscription import Plans,Subscription,SubscriptionPaymentOrder

from domain.fuelflow.registry import Record
from domain.fuelflow.credit import Vehicles,Orders,OrdersLineItem
from domain.fuelflow.unloader import FuelUnloadingBook,FuelDipReader

from infrastructure.persistence.orm.models import AppUsersORM,PlansORM,SubscriptionORM,SubscriptionPaymentOrderORM,AppUserVerificationORM,StoreORM,StoreUserPrivilegeORM,POSORM,StoreActivitiesORM,StoreRolesORM,StoreRotaORM,FuelRegistryORM,StoreCreditVehiclesORM,StoreCreditOrdersORM,StoreCreditOrderLineItemsORM,FuelDipReaderORM,FuelUnloadingBookORM
from datetime import datetime
import uuid
from sqlalchemy import  select
import json
import datetime




def test_infra_orm_credit(session):
    arr=  [uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4(), uuid.uuid4(), uuid.uuid4(), uuid.uuid4(), uuid.uuid4(), uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]
    created=datetime.datetime.now()
    appuser=AppUsers(uid=str(arr[0]), username="testing", phone="testing description",   email="darshan.px@oracle.com", password="SR",   user_type="TTR",is_locked="TESTING",is_verified="TESTING", created_date=created,is_deleted="TESTING")
    store=Store(uid=str(arr[1]), buisness_name="testing",type="testing",address="testing",postal_code="testing", gst_number="testing ",  is_deleted="Y",created_date=created)

    session.add_all([
        StoreORM(**store.dict()),
        AppUsersORM(**appuser.dict())
        ])
    session.commit()
    fdr=FuelDipReader(uid=str(arr[2]), store_uid=str(arr[1]),fuel_tank="testing",dip_number=1.3,liters=2.0)

    session.add_all([
        FuelDipReaderORM(**fdr.dict()),
        ])
    session.commit()


    fub=FuelUnloadingBook(uid=str(arr[2]),
                            store_uid=str(arr[1]),
                            unload_date=created,
                            fuel_tank="testing",
                            vehicle_number="KA0200908",
                            depo_name="Hassan",
                            sample_box="5",
                            before_unload_dip_reading=22,
                            before_unload_liters=22,
                            after_unload_dip_reading=22,
                            after_unload_liters=22,
                            sales=22,
                            bill_density=22,
                            check_density=22,
                            )
    
    session.add_all([
        FuelUnloadingBookORM(**fub.dict()),
        ])
    session.commit()


    records=session.query(FuelUnloadingBookORM).all()
    actual = []
    for l in records:
        actual.append(FuelUnloadingBook.from_orm(l))
    
    assert [fub] == actual



def test_infra_orm_credit(session):
    arr=  [uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4(), uuid.uuid4(), uuid.uuid4(), uuid.uuid4(), uuid.uuid4(), uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]
    created=datetime.datetime.now()
    appuser=AppUsers(uid=str(arr[0]), username="testing", phone="testing description",   email="darshan.px@oracle.com", password="SR",   user_type="TTR",is_locked="TESTING",is_verified="TESTING", created_date=created,is_deleted="TESTING")
    store=Store(uid=str(arr[1]), buisness_name="testing",type="testing",address="testing",postal_code="testing", gst_number="testing ",   is_deleted="Y",created_date=created)

    session.add_all([
        StoreORM(**store.dict()),
        AppUsersORM(**appuser.dict())
        ])
    session.commit()


    storeAdminroles = StoreUserPrivilege( uid=str(arr[3]),
    user_uid=str(arr[0]),
    store_uid=str(arr[1]),
    role="Admin",
    created_date=created,
    updated_date=created)

    session.add_all([
        StoreUserPrivilegeORM(**storeAdminroles.dict()),
        ])
    session.commit()

    privileges=session.query(StoreUserPrivilegeORM).all()
    actual = []

    for l in privileges:
        actual.append(StoreUserPrivilege.from_orm(l))

    storeActivity=StoreActivities(uid=str(arr[2]),store_uid=str(arr[1]),activity_type="testing")
    storeroles=StoreRoles(uid=str(arr[3]),store_uid=str(arr[1]),roles="testing")

    session.add_all([
        StoreActivitiesORM(**storeActivity.dict()),
        StoreRolesORM(**storeroles.dict())
        ])
    session.commit()

    storerota=StoreRota(uid=str(arr[4]),store_uid=str(arr[1]),user_uid= str(arr[0]),from_date=created,till_date=created,role_uid=str(arr[3]),activity_uid=str(arr[2]),approval_status="Approved")


    session.add_all([
        StoreRotaORM(**storerota.dict()),
        ])
    session.commit()


    pos=POS(
        uid=str(arr[5]),
        store_uid=str(arr[1]),
        pos_name="testing",
        pos_type="testing",
        pos_contact_uid=str(arr[0]),
        created_date=created,)

    session.add_all([
    POSORM(**pos.dict())
    ])
    session.commit()


    rota=session.query(StoreRotaORM).all()
    fuelRegistryRecord=Record(
                        uid=str(arr[6]),
                        store_uid=str(arr[1]),
                        pos_uid= str(arr[5]),
                        rota_uid=str(arr[4]),
                        status='Approved',
                        closing_reading=100,
                        opening_reading=100,
                        total_sales=100,
                        rate=100,
                        total=100,
                        cash_amount_received=100,
                        card_amount_received=100,
                        upi_amount_received=100,
                        credits=100,
                        expenditure=100,
                        balance=100,
                    )
    print(fuelRegistryRecord)
    actual = []

    session.add_all([
         FuelRegistryORM(**Record.dict(fuelRegistryRecord))
    ])
    session.commit()

    v=Vehicles(uid=str(arr[7]),store_uid=str(arr[1]),user_uid= str(arr[0]),vehicle_num="KA02-0908",status="Approved")

    session.add_all([
         StoreCreditVehiclesORM(**v.dict())
    ])
    session.commit()

    o=Orders(uid=str(arr[8]),
    store_uid=str(arr[1]),
    pos_uid=str(arr[5]),
    rota_uid=str(arr[4]),
    user_uid= str(arr[0]),
    total_amount=2000,
    type="CREDIT",
    created_date=created)

    session.add_all([
         StoreCreditOrdersORM(**o.dict())
    ])
    session.commit()

    ol=OrdersLineItem(
        uid=str(arr[9]),
        order_id=str(arr[8]),
        vehicle_id=str(arr[7]),
        liters=1200,
        rate=80,
        amount=96000
    )

    session.add_all([
         StoreCreditOrderLineItemsORM(**ol.dict())
    ])
    session.commit()



    records=session.query(StoreCreditOrderLineItemsORM).all()
    actual = []
    for l in records:
        actual.append(OrdersLineItem.from_orm(l))
    
    assert [ol] == actual


def test_infra_orm_fuelRegistry(session):
    arr=  [uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4(), uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]
    created=datetime.datetime.now()
    appuser=AppUsers(uid=str(arr[0]), username="testing", phone="testing description",   email="darshan.px@oracle.com", password="SR",   user_type="TTR",is_locked="TESTING",is_verified="TESTING", created_date=created,is_deleted="TESTING")
    store=Store(uid=str(arr[1]), buisness_name="testing",type="testing",address="testing",postal_code="testing", gst_number="testing ",   is_deleted="Y",created_date=created)

    session.add_all([
        StoreORM(**store.dict()),
        AppUsersORM(**appuser.dict())
        ])
    session.commit()


    storeAdminroles = StoreUserPrivilege( uid=str(arr[3]),
    user_uid=str(arr[0]),
    store_uid=str(arr[1]),
    role="Admin",
    created_date=created,
    updated_date=created)

    session.add_all([
        StoreUserPrivilegeORM(**storeAdminroles.dict()),
        ])
    session.commit()

    privileges=session.query(StoreUserPrivilegeORM).all()
    actual = []

    for l in privileges:
        actual.append(StoreUserPrivilege.from_orm(l))

    storeActivity=StoreActivities(uid=str(arr[2]),store_uid=str(arr[1]),activity_type="testing")
    storeroles=StoreRoles(uid=str(arr[3]),store_uid=str(arr[1]),roles="testing")

    session.add_all([
        StoreActivitiesORM(**storeActivity.dict()),
        StoreRolesORM(**storeroles.dict())
        ])
    session.commit()

    storerota=StoreRota(uid=str(arr[4]),store_uid=str(arr[1]),user_uid= str(arr[0]),from_date=created,till_date=created,role_uid=str(arr[3]),activity_uid=str(arr[2]),approval_status="Approved")


    session.add_all([
        StoreRotaORM(**storerota.dict()),
        ])
    session.commit()


    pos=POS(
        uid=str(arr[5]),
        store_uid=str(arr[1]),
        pos_name="testing",
        pos_type="testing",
        pos_contact_uid=str(arr[0]),
        created_date=created,)

    session.add_all([
    POSORM(**pos.dict())
    ])
    session.commit()


    rota=session.query(StoreRotaORM).all()
    fuelRegistryRecord=Record(
                        uid=str(arr[6]),
                        store_uid=str(arr[1]),
                        pos_uid= str(arr[5]),
                        rota_uid=str(arr[4]),
                        status='Approved',
                        closing_reading=100,
                        opening_reading=100,
                        total_sales=100,
                        rate=100,
                        total=100,
                        cash_amount_received=100,
                        card_amount_received=100,
                        upi_amount_received=100,
                        credits=100,
                        expenditure=100,
                        balance=100,
                    )
    print(fuelRegistryRecord)
    actual = []

    session.add_all([
         FuelRegistryORM(**Record.dict(fuelRegistryRecord))
    ])
    session.commit()
    records=session.query(FuelRegistryORM).all()
    actual = []
    for l in records:
        actual.append(Record.from_orm(l))
    
    assert [fuelRegistryRecord] == actual



def test_infra_orm_subscription(session):
    arr=  [uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4(), uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]
    created=datetime.datetime.now()
    appuser=AppUsers(uid=str(arr[0]), username="testing", phone="testing description",   email="darshan.px@oracle.com", password="SR",   user_type="TTR",is_locked="TESTING",is_verified="TESTING", created_date=created,is_deleted="TESTING")
    store=Store(uid=str(arr[1]), buisness_name="testing",type="testing",address="testing",postal_code="testing", gst_number="testing ",is_deleted="Y",created_date=created)

    session.add_all([
    StoreORM(**store.dict()),
    AppUsersORM(**appuser.dict())
    ])
    session.commit()
    sampleplan1=Plans(uid=str(arr[2]),
                    plan_type='TEST',
                    plan_name='FREE',
                    price=0,
                    period=5,
                    key='testing',
                    retention_limit='5',
                    user_limit='5',
                    status='Active',
                    created_date=created)
    sampleplan2=Plans(uid=str(arr[3]),
                    plan_type='TEST',
                    plan_name='FREE',
                    price=0,
                    period=5,
                    key='testing',
                    retention_limit='5',
                    user_limit='5',
                    status='Active',
                    created_date=created)
    
    session.add_all([
        PlansORM(**sampleplan1.dict()),
        PlansORM(**sampleplan2.dict())
    ])
    session.commit()
    suborder=Subscription(uid=str(arr[4]),
                                store_uid=str(arr[1]),
                                initiated_user_uid=str(arr[0]),
                                plan_id=str(arr[2]),
                                status='testing',
                                created_date=created)
    session.add_all([
        SubscriptionORM(**suborder.dict()),
    ])
    session.commit()

    orders=session.query(SubscriptionORM).all()
    actual = []

    for l in orders:
        actual.append(Subscription.from_orm(l))
    assert [suborder] == actual



def test_infra_orm_store_pos(session):
    arr=  [uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4(), uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]
    created=datetime.datetime.now()
    appuser=AppUsers(uid=str(arr[0]), username="testing", phone="testing description",   email="darshan.px@oracle.com", password="SR",   user_type="TTR",is_locked="TESTING",is_verified="TESTING", created_date=created,is_deleted="TESTING")
    store=Store(uid=str(arr[1]), buisness_name="testing",type="testing",address="testing",postal_code="testing", gst_number="testing ",   is_deleted="Y",created_date=created)

    session.add_all([
    StoreORM(**store.dict()),
    AppUsersORM(**appuser.dict())
    ])
    session.commit()

    pos=POS(uid=str(arr[2]),
        store_uid=str(arr[1]),
        pos_name="testing",
        pos_type="testing",
        pos_contact_uid=str(arr[0]),
        created_date=created,)

    session.add_all([
    POSORM(**pos.dict())
    ])
    session.commit()

    poses=session.query(POSORM).all()
    actual = []

    for l in poses:
        actual.append(POS.from_orm(l))
    assert [pos] == actual


def test_infra_orm_store_rota(session):
    arr=  [uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4(), uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]
    created=datetime.datetime.now()
    appuser=AppUsers(uid=str(arr[0]), username="testing", phone="testing description",   email="darshan.px@oracle.com", password="SR",   user_type="TTR",is_locked="TESTING",is_verified="TESTING", created_date=created,is_deleted="TESTING")
    store=Store(uid=str(arr[1]), buisness_name="testing",type="testing",address="testing",postal_code="testing", gst_number="testing ",   is_deleted="Y",created_date=created)

    session.add_all([
        StoreORM(**store.dict()),
        AppUsersORM(**appuser.dict())
        ])
    session.commit()


    storeAdminroles = StoreUserPrivilege( uid=str(arr[3]),
    user_uid=str(arr[0]),
    store_uid=str(arr[1]),
    role="Admin",
    created_date=created,
    updated_date=created)

    session.add_all([
        StoreUserPrivilegeORM(**storeAdminroles.dict()),
        ])
    session.commit()

    privileges=session.query(StoreUserPrivilegeORM).all()
    actual = []

    for l in privileges:
        actual.append(StoreUserPrivilege.from_orm(l))
    assert [storeAdminroles] == actual

    storeActivity=StoreActivities(uid=str(arr[2]),store_uid=str(arr[1]),activity_type="testing")
    storeroles=StoreRoles(uid=str(arr[3]),store_uid=str(arr[1]),roles="testing")

    session.add_all([
        StoreActivitiesORM(**storeActivity.dict()),
        StoreRolesORM(**storeroles.dict())
        ])
    session.commit()

    storerota=StoreRota(uid=str(arr[4]),store_uid=str(arr[1]),user_uid= str(arr[0]),from_date=created,till_date=created,role_uid=str(arr[3]),activity_uid=str(arr[2]),approval_status="Approved")


    session.add_all([
        StoreRotaORM(**storerota.dict()),
        ])
    session.commit()

    rota=session.query(StoreRotaORM).all()

    print(rota)
    actual = []

    for l in rota:
        actual.append(StoreRota.from_orm(l))
    
    assert [storerota] == actual



def test_infra_orm_store_creation(session):
    arr=  [uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]
    created=datetime.datetime.now()
    store=Store(uid=str(arr[0]),
            buisness_name="testing",
            type="testing",
            address="testing",
            postal_code="testing",
            gst_number="testing ",
            is_deleted="Y",
            created_date=created)
    
    session.add_all([
        StoreORM(**store.dict())
        ])
    
    session.commit()
    stores=session.query(StoreORM).all()
    actual = []

    for l in stores:
        actual.append(Store.from_orm(l))
    
    assert [store] == actual


def  test_infra_orm_appuser_creation(session):
    arr=  [uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]
    created=datetime.datetime.now()
    session.add_all([
        AppUsersORM(uid=str(arr[0]),
                 username="testing",
                 phone="testing description",
                 email="darshan.px@oracle.com",
                 password="SR",
                 user_type="TTR",
                 is_locked="TESTING",
                 is_verified="TESTING", 
                 created_date=created,
                 is_deleted="TESTING"),
    ])
    session.commit()

    
    users=session.query(AppUsersORM).all()
    actual = []
    for rca in users:
        actual.append(AppUsers.from_orm(rca))

    expected = []
    expected.append(AppUsers(
        uid=str(arr[0]),
                 username="testing",
                 phone="testing description",
                 email="darshan.px@oracle.com",
                 password="SR",
                 user_type="TTR",
                 is_locked="TESTING",
                 is_verified="TESTING", 
                 created_date=created,
                 is_deleted="TESTING"
    ))
    assert expected == actual


def test_infra_orm_appuser_verification_code_creation(session):
    arr=  [uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]
    created=datetime.datetime.now()
    app_user = AppUsers(uid=str(arr[0]),
                 username="testing",
                 phone="testing description",
                 email="darshan.px@oracle.com",
                 password="SR",
                 user_type="TTR",
                 is_locked="TESTING",
                 is_verified="TESTING", 
                 created_date=created,
                 is_deleted="TESTING")
    
    session.add_all([
        AppUsersORM(**app_user.dict())  
    ])
    session.commit()

    verification=AppUserVerification(
        uid=str(arr[1]),
        user_uid=str(arr[0]),
        verification_code="qwertry"
     )
    session.add_all([
        AppUserVerificationORM(**verification.dict())
    ])
    session.commit()
    users=session.query(AppUserVerificationORM).all()
    actual = []
    for rca in users:
        actual.append(AppUserVerification.from_orm(rca))

    expected = []
    expected.append(verification)
    assert expected == actual
    
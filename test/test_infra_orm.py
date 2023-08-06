from domain.core.app_users import AppUsers, AppUserVerification
from domain.core.lob import LOB,LOBActivities,LOBRoles,LOBRota,LOBUserPrivilege,POS
from domain.core.subscription import Plans,SubscriptionOrders

from domain.fuel.registry import Record
from domain.fuel.credit import Vehicles,Orders,OrdersLineItem
from domain.fuel.unloader import FuelUnloadingBook,FuelDipReader

from infrastructure.persistence.orm.models import AppUsersORM,PlansORM,SubscriptionOrdersORM,AppUserVerificationORM,LOBORM,LOBUserPrivilegeORM,POSORM,LOBActivitiesORM,LOBRolesORM,LOBRotaORM,FuelRegistryORM,LOBCreditVehiclesORM,LOBCreditOrdersORM,LOBCreditOrderLineItemsORM,FuelDipReaderORM,FuelUnloadingBookORM
from datetime import datetime
import uuid
from sqlalchemy import  select
import json
import datetime




def test_infra_orm_credit(session):
    arr=  [uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4(), uuid.uuid4(), uuid.uuid4(), uuid.uuid4(), uuid.uuid4(), uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]
    created=datetime.datetime.now()
    appuser=AppUsers(uid=str(arr[0]), username="testing", phone="testing description",   email="darshan.px@oracle.com", password="SR",   user_type="TTR",is_locked="TESTING",is_verified="TESTING", created_date=created,is_deleted="TESTING")
    lob=LOB(uid=str(arr[1]), buisness_name="testing",type="testing",address="testing",postal_code="testing", gst_number="testing ", subscription_status="Active",   is_deleted="Y",created_date=created)

    session.add_all([
        LOBORM(**lob.dict()),
        AppUsersORM(**appuser.dict())
        ])
    session.commit()
    fdr=FuelDipReader(uid=str(arr[2]), lob_uid=str(arr[1]),fuel_tank="testing",dip_number=1.3,liters=2.0)

    session.add_all([
        FuelDipReaderORM(**fdr.dict()),
        ])
    session.commit()


    fub=FuelUnloadingBook(uid=str(arr[2]),
                            lob_uid=str(arr[1]),
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
    lob=LOB(uid=str(arr[1]), buisness_name="testing",type="testing",address="testing",postal_code="testing", gst_number="testing ", subscription_status="Active",   is_deleted="Y",created_date=created)

    session.add_all([
        LOBORM(**lob.dict()),
        AppUsersORM(**appuser.dict())
        ])
    session.commit()


    lobAdminroles = LOBUserPrivilege( uid=str(arr[3]),
    user_uid=str(arr[0]),
    lob_uid=str(arr[1]),
    role="Admin",
    created_date=created,
    updated_date=created)

    session.add_all([
        LOBUserPrivilegeORM(**lobAdminroles.dict()),
        ])
    session.commit()

    privileges=session.query(LOBUserPrivilegeORM).all()
    actual = []

    for l in privileges:
        actual.append(LOBUserPrivilege.from_orm(l))

    lobActivity=LOBActivities(uid=str(arr[2]),lob_uid=str(arr[1]),activity_type="testing")
    lobroles=LOBRoles(uid=str(arr[3]),lob_uid=str(arr[1]),roles="testing")

    session.add_all([
        LOBActivitiesORM(**lobActivity.dict()),
        LOBRolesORM(**lobroles.dict())
        ])
    session.commit()

    lobrota=LOBRota(uid=str(arr[4]),lob_uid=str(arr[1]),user_uid= str(arr[0]),from_date=created,till_date=created,role_uid=str(arr[3]),activity_uid=str(arr[2]),approval_status="Approved")


    session.add_all([
        LOBRotaORM(**lobrota.dict()),
        ])
    session.commit()


    pos=POS(
        uid=str(arr[5]),
        lob_uid=str(arr[1]),
        pos_name="testing",
        pos_type="testing",
        pos_contact_uid=str(arr[0]),
        created_date=created,)

    session.add_all([
    POSORM(**pos.dict())
    ])
    session.commit()


    rota=session.query(LOBRotaORM).all()
    fuelRegistryRecord=Record(
                        uid=str(arr[6]),
                        lob_uid=str(arr[1]),
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

    v=Vehicles(uid=str(arr[7]),lob_uid=str(arr[1]),user_uid= str(arr[0]),vehicle_num="KA02-0908",status="Approved")

    session.add_all([
         LOBCreditVehiclesORM(**v.dict())
    ])
    session.commit()

    o=Orders(uid=str(arr[8]),
    lob_uid=str(arr[1]),
    pos_uid=str(arr[5]),
    rota_uid=str(arr[4]),
    user_uid= str(arr[0]),
    total_amount=2000,
    type="CREDIT",
    created_date=created)

    session.add_all([
         LOBCreditOrdersORM(**o.dict())
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
         LOBCreditOrderLineItemsORM(**ol.dict())
    ])
    session.commit()



    records=session.query(LOBCreditOrderLineItemsORM).all()
    actual = []
    for l in records:
        actual.append(OrdersLineItem.from_orm(l))
    
    assert [ol] == actual


def test_infra_orm_fuelRegistry(session):
    arr=  [uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4(), uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]
    created=datetime.datetime.now()
    appuser=AppUsers(uid=str(arr[0]), username="testing", phone="testing description",   email="darshan.px@oracle.com", password="SR",   user_type="TTR",is_locked="TESTING",is_verified="TESTING", created_date=created,is_deleted="TESTING")
    lob=LOB(uid=str(arr[1]), buisness_name="testing",type="testing",address="testing",postal_code="testing", gst_number="testing ", subscription_status="Active",   is_deleted="Y",created_date=created)

    session.add_all([
        LOBORM(**lob.dict()),
        AppUsersORM(**appuser.dict())
        ])
    session.commit()


    lobAdminroles = LOBUserPrivilege( uid=str(arr[3]),
    user_uid=str(arr[0]),
    lob_uid=str(arr[1]),
    role="Admin",
    created_date=created,
    updated_date=created)

    session.add_all([
        LOBUserPrivilegeORM(**lobAdminroles.dict()),
        ])
    session.commit()

    privileges=session.query(LOBUserPrivilegeORM).all()
    actual = []

    for l in privileges:
        actual.append(LOBUserPrivilege.from_orm(l))

    lobActivity=LOBActivities(uid=str(arr[2]),lob_uid=str(arr[1]),activity_type="testing")
    lobroles=LOBRoles(uid=str(arr[3]),lob_uid=str(arr[1]),roles="testing")

    session.add_all([
        LOBActivitiesORM(**lobActivity.dict()),
        LOBRolesORM(**lobroles.dict())
        ])
    session.commit()

    lobrota=LOBRota(uid=str(arr[4]),lob_uid=str(arr[1]),user_uid= str(arr[0]),from_date=created,till_date=created,role_uid=str(arr[3]),activity_uid=str(arr[2]),approval_status="Approved")


    session.add_all([
        LOBRotaORM(**lobrota.dict()),
        ])
    session.commit()


    pos=POS(
        uid=str(arr[5]),
        lob_uid=str(arr[1]),
        pos_name="testing",
        pos_type="testing",
        pos_contact_uid=str(arr[0]),
        created_date=created,)

    session.add_all([
    POSORM(**pos.dict())
    ])
    session.commit()


    rota=session.query(LOBRotaORM).all()
    fuelRegistryRecord=Record(
                        uid=str(arr[6]),
                        lob_uid=str(arr[1]),
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
    lob=LOB(uid=str(arr[1]), buisness_name="testing",type="testing",address="testing",postal_code="testing", gst_number="testing ", subscription_status="Active",   is_deleted="Y",created_date=created)

    session.add_all([
    LOBORM(**lob.dict()),
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
    suborder=SubscriptionOrders(uid=str(arr[4]),
                                lob_uid=str(arr[1]),
                                initiated_user_uid=str(arr[0]),
                                plan_id=str(arr[2]),
                                paid_amount=300,
                                receipt_id='testing',
                                status='testing',
                                payment_id='testing',
                                order_id='testing',
                                signature='testing',
                                created_date=created)
    session.add_all([
        SubscriptionOrdersORM(**suborder.dict()),
    ])
    session.commit()

    orders=session.query(SubscriptionOrdersORM).all()
    actual = []

    for l in orders:
        actual.append(SubscriptionOrders.from_orm(l))
    assert [suborder] == actual



def test_infra_orm_lob_pos(session):
    arr=  [uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4(), uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]
    created=datetime.datetime.now()
    appuser=AppUsers(uid=str(arr[0]), username="testing", phone="testing description",   email="darshan.px@oracle.com", password="SR",   user_type="TTR",is_locked="TESTING",is_verified="TESTING", created_date=created,is_deleted="TESTING")
    lob=LOB(uid=str(arr[1]), buisness_name="testing",type="testing",address="testing",postal_code="testing", gst_number="testing ", subscription_status="Active",   is_deleted="Y",created_date=created)

    session.add_all([
    LOBORM(**lob.dict()),
    AppUsersORM(**appuser.dict())
    ])
    session.commit()

    pos=POS(uid=str(arr[2]),
        lob_uid=str(arr[1]),
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


def test_infra_orm_lob_rota(session):
    arr=  [uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4(), uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]
    created=datetime.datetime.now()
    appuser=AppUsers(uid=str(arr[0]), username="testing", phone="testing description",   email="darshan.px@oracle.com", password="SR",   user_type="TTR",is_locked="TESTING",is_verified="TESTING", created_date=created,is_deleted="TESTING")
    lob=LOB(uid=str(arr[1]), buisness_name="testing",type="testing",address="testing",postal_code="testing", gst_number="testing ", subscription_status="Active",   is_deleted="Y",created_date=created)

    session.add_all([
        LOBORM(**lob.dict()),
        AppUsersORM(**appuser.dict())
        ])
    session.commit()


    lobAdminroles = LOBUserPrivilege( uid=str(arr[3]),
    user_uid=str(arr[0]),
    lob_uid=str(arr[1]),
    role="Admin",
    created_date=created,
    updated_date=created)

    session.add_all([
        LOBUserPrivilegeORM(**lobAdminroles.dict()),
        ])
    session.commit()

    privileges=session.query(LOBUserPrivilegeORM).all()
    actual = []

    for l in privileges:
        actual.append(LOBUserPrivilege.from_orm(l))
    assert [lobAdminroles] == actual

    lobActivity=LOBActivities(uid=str(arr[2]),lob_uid=str(arr[1]),activity_type="testing")
    lobroles=LOBRoles(uid=str(arr[3]),lob_uid=str(arr[1]),roles="testing")

    session.add_all([
        LOBActivitiesORM(**lobActivity.dict()),
        LOBRolesORM(**lobroles.dict())
        ])
    session.commit()

    lobrota=LOBRota(uid=str(arr[4]),lob_uid=str(arr[1]),user_uid= str(arr[0]),from_date=created,till_date=created,role_uid=str(arr[3]),activity_uid=str(arr[2]),approval_status="Approved")


    session.add_all([
        LOBRotaORM(**lobrota.dict()),
        ])
    session.commit()

    rota=session.query(LOBRotaORM).all()

    print(rota)
    actual = []

    for l in rota:
        actual.append(LOBRota.from_orm(l))
    
    assert [lobrota] == actual



def test_infra_orm_lob_creation(session):
    arr=  [uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]
    created=datetime.datetime.now()
    lob=LOB(uid=str(arr[0]),
            buisness_name="testing",
            type="testing",
            address="testing",
            postal_code="testing",
            gst_number="testing ",
            subscription_status="Active",   
            is_deleted="Y",
            created_date=created)
    
    session.add_all([
        LOBORM(**lob.dict())
        ])
    
    session.commit()
    lobs=session.query(LOBORM).all()
    actual = []

    for l in lobs:
        actual.append(LOB.from_orm(l))
    
    assert [lob] == actual


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
    
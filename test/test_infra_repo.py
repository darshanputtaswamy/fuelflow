from domain.core.app_users import AppUsers,AppUserVerification
from domain.fuelflow.store import Store,StoreActivities,StoreRoles,StoreRota,StoreUserPrivilege,POS
from domain.core.subscription import Plans, Subscription,SubscriptionPaymentOrder
from infrastructure.repository.core.app_users_sa_repo import AppUsersSQLAlchemyRepository
from infrastructure.repository.fuelflow.store_sa_repo import StoreSQLAlchemyRepository,StoreActivitiesSQLAlchemyRepository,StoreRolesSQLAlchemyRepository,StoreUserPrivilegeSQLAlchemyRepository,StoreRotaSQLAlchemyRepository,POSSQLAlchemyRepository
from infrastructure.repository.core.subscription_sa_repo import PlansSQLAlchemyRepository,SubscriptionSQLAlchemyRepository, SubscriptionPaymentOrderSQLAlchemyRepository

from infrastructure.persistence.orm.models import AppUsersORM,PlansORM,SubscriptionORM,SubscriptionPaymentOrderORM,AppUserVerificationORM,StoreORM,StoreUserPrivilegeORM,POSORM,StoreActivitiesORM,StoreRolesORM,StoreRotaORM,FuelRegistryORM,StoreCreditVehiclesORM,StoreCreditOrdersORM,StoreCreditOrderLineItemsORM,FuelDipReaderORM,FuelUnloadingBookORM
from datetime import datetime
import uuid
from sqlalchemy import  select
import json
import datetime
import string 
import random



def test_infra_subscription_curd(session):
    arr=  [uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]
    created=datetime.datetime.now()

    AppuserObj= AppUsers(uid=str(arr[0]),username="testing",phone="testing description",email="darshan.px@oracle.com",password="SR",user_type="TTR",is_locked="TESTING",is_verified="TESTING", created_date=created,is_deleted="TESTING")
    repo = AppUsersSQLAlchemyRepository(session)
    repo.add(AppuserObj)
    session.commit()

    storeObj=Store(uid=str(arr[1]), buisness_name="testing",type="testing",address="testing",postal_code="testing", gst_number="testing ",   is_deleted="N",created_date=created)
    storerepo = StoreSQLAlchemyRepository(session)
    storerepo.add(storeObj)
    session.commit()


    planObj=Plans(uid=str(arr[2]), plan_type="testing",plan_name="testing",price=1,period=1, key="testing ", retention_limit=1,   user_limit=1,status="Approved",created_date=created)
    planrepo = PlansSQLAlchemyRepository(session)
    planrepo.add(planObj)
    session.commit()

    subObj=Subscription(uid=str(arr[3]),store_uid=str(arr[1]),initiated_user_uid=str(arr[0]),plan_id=str(arr[2]),paid_amount=1,receipt_id="1212",status="Pending",payment_id="testing",order_id="testing",signature="testing",created_date=created)

    subRepo = SubscriptionSQLAlchemyRepository(session)
    subRepo.add(subObj)
    session.commit()


    subs=session.query(SubscriptionORM).all()
    actual = []
    for p in subs:
        actual.append(Subscription.from_orm(p))

    expected = []
    expected.append(subObj)
    assert expected == actual


    res = subRepo.getByReference(store_uid=str(arr[1]))
    assert res == expected

    res = subRepo.list()
    assert res == expected

    res = subRepo.get(id=str(arr[3]))
    assert res == subObj

    subObj.status="Complete"

    res = subRepo.update(subObj)
    session.commit()

    res = subRepo.get(id=str(arr[3]))
    assert res == subObj


def test_infra_plan_curd(session):
    arr=  [uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]
    created=datetime.datetime.now()



    planObj=Plans(uid=str(arr[2]), plan_type="testing",plan_name="testing",price=1,period=1, key="testing ", retention_limit=1,   user_limit=1,status="Approved",created_date=created)
    planrepo = PlansSQLAlchemyRepository(session)
    planrepo.add(planObj)
    session.commit()

    plans=session.query(PlansORM).all()
    actual = []
    for p in plans:
        actual.append(Plans.from_orm(p))

    expected = []
    expected.append(planObj)
    assert expected == actual


    res = planrepo.getByReference(plan_name="testing")
    assert res == expected

    res = planrepo.list()
    assert res == expected

    res = planrepo.get(id=str(arr[2]))
    assert res == planObj

    planObj.plan_type="Testing2"

    res = planrepo.update(planObj)
    session.commit()

    res = planrepo.get(id=str(arr[2]))
    assert res == planObj


def test_infra_storepos_curd(session):
    arr=  [uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]
    created=datetime.datetime.now()

    AppuserObj= AppUsers(uid=str(arr[0]),username="testing",phone="testing description",email="darshan.px@oracle.com",password="SR",user_type="TTR",is_locked="TESTING",is_verified="TESTING", created_date=created,is_deleted="TESTING")
    repo = AppUsersSQLAlchemyRepository(session)
    repo.add(AppuserObj)
    session.commit()

    storeObj=Store(uid=str(arr[1]), buisness_name="testing",type="testing",address="testing",postal_code="testing", gst_number="testing ",   is_deleted="N",created_date=created)
    storerepo = StoreSQLAlchemyRepository(session)
    storerepo.add(storeObj)
    session.commit()


    storepos=POS(uid=str(arr[2]), store_uid=str(arr[1]),pos_contact_uid=str(arr[0]), pos_name='=str(arr[0])',pos_type='Testing' ,created_date=created)
    storePosRepo = POSSQLAlchemyRepository(session)
    storePosRepo.add(storepos)
    session.commit()


    storePOSs=session.query(POSORM).all()
    actual = []
    for rca in storePOSs:
        actual.append(POS.from_orm(rca))

    expected = []
    expected.append(storepos)
    assert expected == actual


    res = storePosRepo.getByReference(store_uid=str(arr[1]))
    assert res == expected

    res = storePosRepo.list()
    assert res == expected

    res = storePosRepo.get(id=str(arr[2]))
    assert res == storepos

    storepos.pos_type="Testing2"

    res = storePosRepo.update(storepos)
    session.commit()

    res = storePosRepo.get(id=str(arr[2]))
    assert res == storepos




def test_infra_storerota_curd(session):
    arr=  [uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]
    created=datetime.datetime.now()

    AppuserObj= AppUsers(uid=str(arr[0]),username="testing",phone="testing description",email="darshan.px@oracle.com",password="SR",user_type="TTR",is_locked="TESTING",is_verified="TESTING", created_date=created,is_deleted="TESTING")
    repo = AppUsersSQLAlchemyRepository(session)
    repo.add(AppuserObj)
    session.commit()

    storeObj=Store(uid=str(arr[1]), buisness_name="testing",type="testing",address="testing",postal_code="testing", gst_number="testing ",   is_deleted="N",created_date=created)
    storerepo = StoreSQLAlchemyRepository(session)
    storerepo.add(storeObj)
    session.commit()

    storeRole=StoreRoles(uid=str(arr[2]), store_uid=str(arr[1]), roles='ADMIN')
    storeRolerepo = StoreRolesSQLAlchemyRepository(session)
    storeRolerepo.add(storeRole)
    session.commit()

    storeActivity=StoreActivities(uid=str(arr[3]), store_uid=str(arr[1]), activity_type='ADMIN')
    storeActivityrepo = StoreActivitiesSQLAlchemyRepository(session)
    storeActivityrepo.add(storeActivity)
    session.commit()


    storeRota=StoreRota(uid=str(arr[3]), store_uid=str(arr[1]), user_uid=str(arr[0]),from_date=created ,till_date=created,role_uid=str(arr[2]),activity_uid=str(arr[3]),approval_status='Approved')
    storeRotaRepo = StoreRotaSQLAlchemyRepository(session)
    storeRotaRepo.add(storeRota)
    session.commit()


    storeRotas=session.query(StoreRotaORM).all()
    actual = []
    for rca in storeRotas:
        actual.append(StoreRota.from_orm(rca))

    expected = []
    expected.append(storeRota)
    assert expected == actual


    res = storeRotaRepo.getByReference(store_uid=str(arr[1]))
    assert res == expected

    res = storeRotaRepo.list()
    assert res == expected

    res = storeRotaRepo.get(id=str(arr[3]))
    assert res == storeRota

    storeRota.approval_status="DENIED"

    res = storeRotaRepo.update(storeRota)
    session.commit()

    res = storeRotaRepo.get(id=str(arr[3]))
    assert res == storeRota




def test_infra_repo_storeRoles_crud(session):
    arr=  [uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]
    created=datetime.datetime.now()
    storeObj=Store(uid=str(arr[1]), buisness_name="testing",type="testing",address="testing",postal_code="testing", gst_number="testing ",   is_deleted="N",created_date=created)
    storerepo = StoreSQLAlchemyRepository(session)
    storerepo.add(storeObj)
    session.commit()

    storeRole=StoreRoles(uid=str(arr[2]), store_uid=str(arr[1]), roles='ADMIN')
    storeRolerepo = StoreRolesSQLAlchemyRepository(session)
    storeRolerepo.add(storeRole)
    session.commit()


    storeActivities=session.query(StoreRolesORM).all()
    actual = []
    for rca in storeActivities:
        actual.append(StoreRoles.from_orm(rca))

    expected = []
    expected.append(storeRole)
    assert expected == actual


    res = storeRolerepo.getByReference(store_uid=str(arr[1]))
    assert res == expected

    res = storeRolerepo.list()
    assert res == expected

    res = storeRolerepo.get(id=str(arr[2]))
    assert res == storeRole



def test_infra_repo_storeActivities_crud(session):
    arr=  [uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]
    created=datetime.datetime.now()
    storeObj=Store(uid=str(arr[1]), buisness_name="testing",type="testing",address="testing",postal_code="testing", gst_number="testing ",   is_deleted="N",created_date=created)
    storerepo = StoreSQLAlchemyRepository(session)
    storerepo.add(storeObj)
    session.commit()

    storeActivity=StoreActivities(uid=str(arr[2]), store_uid=str(arr[1]), activity_type='ADMIN')
    storeActivityrepo = StoreActivitiesSQLAlchemyRepository(session)
    storeActivityrepo.add(storeActivity)
    session.commit()


    storeActivities=session.query(StoreActivitiesORM).all()
    actual = []
    for rca in storeActivities:
        actual.append(StoreActivities.from_orm(rca))

    expected = []
    expected.append(storeActivity)
    assert expected == actual


    res = storeActivityrepo.getByReference(store_uid=str(arr[1]))
    assert res == expected

    res = storeActivityrepo.list()
    assert res == expected

    res = storeActivityrepo.get(id=str(arr[2]))
    assert res == storeActivity




def test_infra_repo_storeUserPrivilege_crud(session):
    arr=  [uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]
    created=datetime.datetime.now()
    AppuserObj= AppUsers(uid=str(arr[0]),
                    username="testing",
                    phone="testing description",
                    email="darshan.px@oracle.com",
                    password="SR",
                    user_type="TTR",
                    is_locked="TESTING",
                    is_verified="TESTING", 
                    created_date=created,
                    is_deleted="TESTING")

    repo = AppUsersSQLAlchemyRepository(session)
    repo.add(AppuserObj)
    session.commit()

    storeObj=Store(uid=str(arr[1]), buisness_name="testing",type="testing",address="testing",postal_code="testing", gst_number="testing ",  is_deleted="N",created_date=created)
    storerepo = StoreSQLAlchemyRepository(session)
    storerepo.add(storeObj)
    session.commit()

    storePriv=StoreUserPrivilege(uid=str(arr[2]), user_uid=str(arr[0]), store_uid=str(arr[1]),role='ADMIN',created_date=created)
    storePrivrepo = StoreUserPrivilegeSQLAlchemyRepository(session)
    storePrivrepo.add(storePriv)
    session.commit()


    storePrivs=session.query(StoreUserPrivilegeORM).all()
    actual = []
    for rca in storePrivs:
        actual.append(StoreUserPrivilege.from_orm(rca))

    expected = []
    expected.append(storePriv)
    assert expected == actual


    res = storePrivrepo.getByReference(store_uid=str(arr[1]))
    assert res == expected

    res = storePrivrepo.list()
    assert res == expected

    res = storePrivrepo.get(id=str(arr[2]))
    assert res == storePriv

    storePriv.role="EMPLOYEE"

    res = storePrivrepo.update(storePriv)
    session.commit()

    res = storePrivrepo.get(id=str(arr[2]))
    assert res == storePriv



def test_infra_repo_store_crud(session):
    arr=  [uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]
    created=datetime.datetime.now()


    storeObj=Store(uid=str(arr[1]), buisness_name="testing",type="testing",address="testing",postal_code="testing", gst_number="testing ",  is_deleted="N",created_date=created)
    storerepo = StoreSQLAlchemyRepository(session)
    storerepo.add(storeObj)
    session.commit()


    users=session.query(StoreORM).all()
    actual = []
    for rca in users:
        actual.append(Store.from_orm(rca))

    expected = []
    expected.append(storeObj)
    assert expected == actual


    res = storerepo.getByReference(buisness_name="testing")
    assert res == expected

    res = storerepo.list()
    assert res == expected

    res = storerepo.get(id=str(arr[1]))
    assert res == storeObj

    storeObj.buisness_name="another_name"

    res = storerepo.update(storeObj)
    session.commit()

    res = storerepo.get(id=str(arr[1]))
    assert res == storeObj




def test_infra_repo_appuser_crud(session):
    arr=  [uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]
    created=datetime.datetime.now()
    AppuserObj= AppUsers(uid=str(arr[0]),
                 username="testing",
                 phone="testing description",
                 email="darshan.px@oracle.com",
                 password="SR",
                 user_type="TTR",
                 is_locked="TESTING",
                 is_verified="TESTING", 
                 created_date=created,
                 is_deleted="TESTING")
    
    repo = AppUsersSQLAlchemyRepository(session)
    repo.add(AppuserObj)
    session.commit()

    users=session.query(AppUsersORM).all()
    actual = []
    for rca in users:
        actual.append(AppUsers.from_orm(rca))

    expected = []
    expected.append(AppuserObj)
    assert expected == actual


    res = repo.getByReference(username="testing")
    assert res == expected

    res = repo.list()
    assert res == expected

    res = repo.get(id=str(arr[0]))
    assert res == AppuserObj

    AppuserObj.username="another_name"

    res = repo.update(AppuserObj)
    session.commit()

    res = repo.get(id=str(arr[0]))
    assert res == AppuserObj



def __generate_random_string(length):
    # Define the characters you want to include in the random string
    characters = string.ascii_letters + string.digits  # includes uppercase and lowercase letters, and digits
    
    # Generate the random string
    random_string = ''.join(random.choice(characters) for _ in range(length))
    
    return random_string

def test_infra_repo_appuser_verification_curd(session):
    arr=  [uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]
    created=datetime.datetime.now()
    AppuserObj= AppUsers(uid=str(arr[0]),
                 username="testing",
                 phone="testing description",
                 email="darshan.px@oracle.com",
                 password="SR",
                 user_type="TTR",
                 is_locked="TESTING",
                 is_verified="TESTING", 
                 created_date=created,
                 is_deleted="TESTING")
    
    repo = AppUsersSQLAlchemyRepository(session)
    repo.add(AppuserObj)
    session.commit()

    res= repo.getVerificationCode(user_uid=str(arr[0]))
    assert res == []

    UVObject = AppUserVerification(uid=str(arr[1]),user_uid=str(arr[0]),verification_code=__generate_random_string(5))
    res= repo.saveVerificationCode(UVObject)
    session.commit()


    res= repo.getVerificationCode(user_uid=str(arr[0]))
    print(UVObject)
    assert res == [UVObject]
    

    res= repo.deleteVerificationCode(uid=UVObject.uid)
    session.commit()

    res= repo.getVerificationCode(user_uid=str(arr[0]))
    assert res == []


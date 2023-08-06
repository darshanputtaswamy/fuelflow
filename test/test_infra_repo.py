from domain.core.app_users import AppUsers,AppUserVerification
from domain.fuel.lob import LOB,LOBActivities,LOBRoles,LOBRota,LOBUserPrivilege,POS
from domain.core.subscription import Plans, SubscriptionOrders
from infrastructure.repository.core.app_users_sa_repo import AppUsersSQLAlchemyRepository
from infrastructure.repository.fuel.lob_sa_repo import LOBSQLAlchemyRepository,LOBActivitiesSQLAlchemyRepository,LOBRolesSQLAlchemyRepository,LOBUserPrivilegeSQLAlchemyRepository,LOBRotaSQLAlchemyRepository,POSSQLAlchemyRepository
from infrastructure.repository.core.subscription_sa_repo import PlansSQLAlchemyRepository,SubscriptionOrdersSQLAlchemyRepository

from infrastructure.persistence.orm.models import AppUsersORM,PlansORM,SubscriptionOrdersORM,AppUserVerificationORM,LOBORM,LOBUserPrivilegeORM,POSORM,LOBActivitiesORM,LOBRolesORM,LOBRotaORM,FuelRegistryORM,LOBCreditVehiclesORM,LOBCreditOrdersORM,LOBCreditOrderLineItemsORM,FuelDipReaderORM,FuelUnloadingBookORM
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

    lobObj=LOB(uid=str(arr[1]), buisness_name="testing",type="testing",address="testing",postal_code="testing", gst_number="testing ",   is_deleted="N",created_date=created)
    lobrepo = LOBSQLAlchemyRepository(session)
    lobrepo.add(lobObj)
    session.commit()


    planObj=Plans(uid=str(arr[2]), plan_type="testing",plan_name="testing",price=1,period=1, key="testing ", retention_limit=1,   user_limit=1,status="Approved",created_date=created)
    planrepo = PlansSQLAlchemyRepository(session)
    planrepo.add(planObj)
    session.commit()

    subObj=SubscriptionOrders(uid=str(arr[3]),lob_uid=str(arr[1]),initiated_user_uid=str(arr[0]),plan_id=str(arr[2]),paid_amount=1,receipt_id="1212",status="Pending",payment_id="testing",order_id="testing",signature="testing",created_date=created)

    subRepo = SubscriptionOrdersSQLAlchemyRepository(session)
    subRepo.add(subObj)
    session.commit()


    subs=session.query(SubscriptionOrdersORM).all()
    actual = []
    for p in subs:
        actual.append(SubscriptionOrders.from_orm(p))

    expected = []
    expected.append(subObj)
    assert expected == actual


    res = subRepo.getByReference(lob_uid=str(arr[1]))
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


def test_infra_lobpos_curd(session):
    arr=  [uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]
    created=datetime.datetime.now()

    AppuserObj= AppUsers(uid=str(arr[0]),username="testing",phone="testing description",email="darshan.px@oracle.com",password="SR",user_type="TTR",is_locked="TESTING",is_verified="TESTING", created_date=created,is_deleted="TESTING")
    repo = AppUsersSQLAlchemyRepository(session)
    repo.add(AppuserObj)
    session.commit()

    lobObj=LOB(uid=str(arr[1]), buisness_name="testing",type="testing",address="testing",postal_code="testing", gst_number="testing ",   is_deleted="N",created_date=created)
    lobrepo = LOBSQLAlchemyRepository(session)
    lobrepo.add(lobObj)
    session.commit()


    lobpos=POS(uid=str(arr[2]), lob_uid=str(arr[1]),pos_contact_uid=str(arr[0]), pos_name='=str(arr[0])',pos_type='Testing' ,created_date=created)
    lobPosRepo = POSSQLAlchemyRepository(session)
    lobPosRepo.add(lobpos)
    session.commit()


    lobPOSs=session.query(POSORM).all()
    actual = []
    for rca in lobPOSs:
        actual.append(POS.from_orm(rca))

    expected = []
    expected.append(lobpos)
    assert expected == actual


    res = lobPosRepo.getByReference(lob_uid=str(arr[1]))
    assert res == expected

    res = lobPosRepo.list()
    assert res == expected

    res = lobPosRepo.get(id=str(arr[2]))
    assert res == lobpos

    lobpos.pos_type="Testing2"

    res = lobPosRepo.update(lobpos)
    session.commit()

    res = lobPosRepo.get(id=str(arr[2]))
    assert res == lobpos




def test_infra_lobrota_curd(session):
    arr=  [uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]
    created=datetime.datetime.now()

    AppuserObj= AppUsers(uid=str(arr[0]),username="testing",phone="testing description",email="darshan.px@oracle.com",password="SR",user_type="TTR",is_locked="TESTING",is_verified="TESTING", created_date=created,is_deleted="TESTING")
    repo = AppUsersSQLAlchemyRepository(session)
    repo.add(AppuserObj)
    session.commit()

    lobObj=LOB(uid=str(arr[1]), buisness_name="testing",type="testing",address="testing",postal_code="testing", gst_number="testing ",   is_deleted="N",created_date=created)
    lobrepo = LOBSQLAlchemyRepository(session)
    lobrepo.add(lobObj)
    session.commit()

    lobRole=LOBRoles(uid=str(arr[2]), lob_uid=str(arr[1]), roles='ADMIN')
    lobRolerepo = LOBRolesSQLAlchemyRepository(session)
    lobRolerepo.add(lobRole)
    session.commit()

    lobActivity=LOBActivities(uid=str(arr[3]), lob_uid=str(arr[1]), activity_type='ADMIN')
    lobActivityrepo = LOBActivitiesSQLAlchemyRepository(session)
    lobActivityrepo.add(lobActivity)
    session.commit()


    lobRota=LOBRota(uid=str(arr[3]), lob_uid=str(arr[1]), user_uid=str(arr[0]),from_date=created ,till_date=created,role_uid=str(arr[2]),activity_uid=str(arr[3]),approval_status='Approved')
    lobRotaRepo = LOBRotaSQLAlchemyRepository(session)
    lobRotaRepo.add(lobRota)
    session.commit()


    lobRotas=session.query(LOBRotaORM).all()
    actual = []
    for rca in lobRotas:
        actual.append(LOBRota.from_orm(rca))

    expected = []
    expected.append(lobRota)
    assert expected == actual


    res = lobRotaRepo.getByReference(lob_uid=str(arr[1]))
    assert res == expected

    res = lobRotaRepo.list()
    assert res == expected

    res = lobRotaRepo.get(id=str(arr[3]))
    assert res == lobRota

    lobRota.approval_status="DENIED"

    res = lobRotaRepo.update(lobRota)
    session.commit()

    res = lobRotaRepo.get(id=str(arr[3]))
    assert res == lobRota




def test_infra_repo_lobRoles_crud(session):
    arr=  [uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]
    created=datetime.datetime.now()
    lobObj=LOB(uid=str(arr[1]), buisness_name="testing",type="testing",address="testing",postal_code="testing", gst_number="testing ",   is_deleted="N",created_date=created)
    lobrepo = LOBSQLAlchemyRepository(session)
    lobrepo.add(lobObj)
    session.commit()

    lobRole=LOBRoles(uid=str(arr[2]), lob_uid=str(arr[1]), roles='ADMIN')
    lobRolerepo = LOBRolesSQLAlchemyRepository(session)
    lobRolerepo.add(lobRole)
    session.commit()


    lobActivities=session.query(LOBRolesORM).all()
    actual = []
    for rca in lobActivities:
        actual.append(LOBRoles.from_orm(rca))

    expected = []
    expected.append(lobRole)
    assert expected == actual


    res = lobRolerepo.getByReference(lob_uid=str(arr[1]))
    assert res == expected

    res = lobRolerepo.list()
    assert res == expected

    res = lobRolerepo.get(id=str(arr[2]))
    assert res == lobRole



def test_infra_repo_lobActivities_crud(session):
    arr=  [uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]
    created=datetime.datetime.now()
    lobObj=LOB(uid=str(arr[1]), buisness_name="testing",type="testing",address="testing",postal_code="testing", gst_number="testing ",   is_deleted="N",created_date=created)
    lobrepo = LOBSQLAlchemyRepository(session)
    lobrepo.add(lobObj)
    session.commit()

    lobActivity=LOBActivities(uid=str(arr[2]), lob_uid=str(arr[1]), activity_type='ADMIN')
    lobActivityrepo = LOBActivitiesSQLAlchemyRepository(session)
    lobActivityrepo.add(lobActivity)
    session.commit()


    lobActivities=session.query(LOBActivitiesORM).all()
    actual = []
    for rca in lobActivities:
        actual.append(LOBActivities.from_orm(rca))

    expected = []
    expected.append(lobActivity)
    assert expected == actual


    res = lobActivityrepo.getByReference(lob_uid=str(arr[1]))
    assert res == expected

    res = lobActivityrepo.list()
    assert res == expected

    res = lobActivityrepo.get(id=str(arr[2]))
    assert res == lobActivity




def test_infra_repo_lobUserPrivilege_crud(session):
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

    lobObj=LOB(uid=str(arr[1]), buisness_name="testing",type="testing",address="testing",postal_code="testing", gst_number="testing ",  is_deleted="N",created_date=created)
    lobrepo = LOBSQLAlchemyRepository(session)
    lobrepo.add(lobObj)
    session.commit()

    lobPriv=LOBUserPrivilege(uid=str(arr[2]), user_uid=str(arr[0]), lob_uid=str(arr[1]),role='ADMIN',created_date=created)
    lobPrivrepo = LOBUserPrivilegeSQLAlchemyRepository(session)
    lobPrivrepo.add(lobPriv)
    session.commit()


    lobPrivs=session.query(LOBUserPrivilegeORM).all()
    actual = []
    for rca in lobPrivs:
        actual.append(LOBUserPrivilege.from_orm(rca))

    expected = []
    expected.append(lobPriv)
    assert expected == actual


    res = lobPrivrepo.getByReference(lob_uid=str(arr[1]))
    assert res == expected

    res = lobPrivrepo.list()
    assert res == expected

    res = lobPrivrepo.get(id=str(arr[2]))
    assert res == lobPriv

    lobPriv.role="EMPLOYEE"

    res = lobPrivrepo.update(lobPriv)
    session.commit()

    res = lobPrivrepo.get(id=str(arr[2]))
    assert res == lobPriv



def test_infra_repo_lob_crud(session):
    arr=  [uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4(),uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]
    created=datetime.datetime.now()


    lobObj=LOB(uid=str(arr[1]), buisness_name="testing",type="testing",address="testing",postal_code="testing", gst_number="testing ",  is_deleted="N",created_date=created)
    lobrepo = LOBSQLAlchemyRepository(session)
    lobrepo.add(lobObj)
    session.commit()


    users=session.query(LOBORM).all()
    actual = []
    for rca in users:
        actual.append(LOB.from_orm(rca))

    expected = []
    expected.append(lobObj)
    assert expected == actual


    res = lobrepo.getByReference(buisness_name="testing")
    assert res == expected

    res = lobrepo.list()
    assert res == expected

    res = lobrepo.get(id=str(arr[1]))
    assert res == lobObj

    lobObj.buisness_name="another_name"

    res = lobrepo.update(lobObj)
    session.commit()

    res = lobrepo.get(id=str(arr[1]))
    assert res == lobObj




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


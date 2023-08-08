from domain.core.subscription import Plans,Subscription,SubscriptionPaymentOrder, SubscriptionStatus,PlanType
import uuid
import datetime

class SubscriptionService:
    def __init__(self,uow):
        self.uow=uow

    def create_plan(self,plan_type,plan_name,price,period,key,retention_limit,user_limit,status):
        created=datetime.datetime.now()            
        id=uuid.uuid4()
        plan=Plans(uid=str(id),plan_type=plan_type,plan_name=plan_name,price=price,period=period, key=key, retention_limit=retention_limit, user_limit=user_limit,status=status,created_date=created)

        with self.uow:
            self.uow.plans.add(plan)
            self.uow.commit()
            return id
        
    def update_plan(self,id,plan_type,plan_name,price,period,key,retention_limit,user_limit,status):
        with self.uow:
            plan = self.uow.plans.get(id) 
            if not plan:
                raise Exception("Plan "+plan+" not found")
            plan.plan_type=plan_type
            plan.plan_name=plan_name
            plan.price=price
            plan.period=period
            plan.key=key
            plan.retention_limit=retention_limit
            plan.user_limit=user_limit
            plan.status=status
            self.uow.plans.update(plan)
            self.uow.commit()
        

    def delete_plan(self,uid):
        with self.uow:
            plans = self.uow.plans.get(id=uid) 
            if not plans:
                raise Exception("Plan "+id+" not found")
            self.uow.plans.delete(uid)
            self.uow.commit()

    def get_plan_by_id(self,uid):
        with self.uow:
            plans= self.uow.plans.get(id=uid) 
            if  not plans:
                raise Exception("plan not found")
        return plans 


    def get_plans(self):
        with self.uow:
            plans= self.uow.plans.list() 
            if len(plans) == 0:
                raise Exception("plans not found")
        return plans
    
    def check_subscription_renewal_eligibility(self,lob_uid):
        # no subscription in status pending 
        # current subscription plan is close to it's end date 
        created=datetime.datetime.now()
        pending_sub = self.uow.subscription.getByReference(lob_id=lob_uid, status='Pending') 
        if len(pending_sub) >= 1:
            return False

        active_sub = self.uow.subscription.getByReference(lob_id=lob_uid,  status='Active') 

        if len(pending_sub) == 0 and len(active_sub) == 1:
            plan=self.uow.plans.get(id=active_sub[0].plan_id) 
            if ((plan.period + 3 + active_sub[0].plan_start_date)  ==  created):
                return True
            else:
                return False 

        return False

    def create_subscription(self,lob_uid,initiated_user_uid,plan_id):

        with self.uow:
            created=datetime.datetime.now()            
            id=uuid.uuid4()
            status='PENDING'
            plans= self.uow.plans.get(id=plan_id) 
            if  not plans:
                raise Exception("plan not found")
            user= self.uow.user.get(id=initiated_user_uid) 
            if  not user:
                raise Exception("User not found")
            lob= self.uow.lob.get(id=lob_uid) 
            if  not lob:
                raise Exception("Store not found")
            if plans.name == 'FREE':
                status='ACTIVE'
            if (self.check_subscription_renewal_eligibility(lob_uid)):
                sub=Subscription(   uid=str(id),
                                    lob_uid=lob_uid,
                                    initiated_user_uid=initiated_user_uid,
                                    plan_id=plan_id,
                                    status=status, 
                                    created_date=created)
                self.uow.subscription.add(sub)
                self.uow.commit()
        return sub 

    def get_subscription_by_id(self,subscription_uid):
        return self.uow.subscription.get(id=subscription_uid)
    

    def delete_pending_subscription(self,lob_uid,subscription_uid):
        with self.uow:
            sub = self.uow.subscription.getByReference(lob_uid=lob_uid, uid=subscription_uid, status="PENDING") 
            if len(sub)==0:
                raise Exception(subscription_uid+" not found")
            self.uow.subscription.delete(sub.uid)
            self.uow.commit()
        return
    
    def get_subscription(self,lob_uid,status):
        if lob_uid:
            if not status:
                return self.uow.subscription.getByReference(lob_id=lob_uid) 
            else:
                return self.uow.subscription.getByReference(lob_id=lob_uid, status=status.upper()) 
        else:
            if not status:
                return self.uow.subscription.list() 
            else:
                return self.uow.subscription.getByReference(status=status.upper()) 
    

    def create_payment_order(self,subscription_uid,receipt_id,payable_amount,order_id,signature,status):
        with self.uow:
            sub = self.uow.subscription.get(id=subscription_uid, status='PENDING')
            created=datetime.datetime.now()            
            id=uuid.uuid4()
            if not sub:
                raise Exception("Not a vaild subscription for payment")
            payment=SubscriptionPaymentOrder(
                                uid=str(id),
                                subscription_uid=subscription_uid,
                                payable_amount=payable_amount,
                                payment_id=str(id), 
                                signature=signature,
                                status='PENDING PAYMENT',
                                created_date=created)
            self.uow.payment.add(payment)
            self.uow.commit()
        return payment 

    def get_payment_order_by_receipt(self,receipt_id):
        with self.uow:
            order = self.uow.payment.get(id=receipt_id)
            if not order:
                raise Exception("Not a vaild order ")
        return order 

    def payment_verifed_start_subscription(self,subscription_uid,sub_payment_order_uid):
        with self.uow:
            updated=datetime.datetime.now()
            order = self.uow.payment.get(id=sub_payment_order_uid)
            if not order:
                raise Exception("Not a vaild order ")
            sub = self.uow.subscription.get(id=subscription_uid)
            if not sub:
                raise Exception("Not a vaild sub ")
            order.status='PAYMENT RECEIVED'
            order.updated_date=updated
            sub.status='ACTIVE'
            sub.updated_date=updated

            self.uow.subscription.update(sub)
            self.uow.payment.update(order)
            self.uow.commit()
        return order 
        

    def exipre_subscription(self,sub_id):
        with self.uow:
            sub= self.uow.subscription.get(id=sub_id)
            sub.status='EXPIRED'
            self.uow.subscription.update(sub)
            self.uow.commit()
        return sub
    
    '''
    def daily routine to expire subscription 


    def daily route to run notification 
    '''
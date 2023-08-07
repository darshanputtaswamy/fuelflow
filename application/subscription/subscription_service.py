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


    def create_subscription(self,lob_uid,initiated_user_uid,plan_id):

        with self.uow:
            created=datetime.datetime.now()            
            id=uuid.uuid4()
            status='Pending'
            plans= self.uow.plans.get(id=plan_id) 
            if  not plans:
                raise Exception("plan not found")
            user= self.uow.user.get(id=initiated_user_uid) 
            if  not user:
                raise Exception("User not found")
            lob= self.uow.lob.get(id=lob_uid) 
            if  not lob:
                raise Exception("Store not found")
            if plans.name == 'free':
                status='active'
            if (check_subscription_renewal_eligibility(lob_uid,plan_id)):
                sub=Subscription(   uid=str(id),
                                    lob_uid=lob_uid,
                                    initiated_user_uid=initiated_user_uid,
                                    plan_id=plan_id,
                                    status=status, 
                                    created_date=created)
                self.uow.subscription.add(sub)
                self.uow.commit()
        return sub 

    def get_pending_subscription(self,lob_uid):
        sub = self.uow.subscription.getByReference(lob_id=lob_uid, status='Pending') 
        if len(sub) == 0:
            return None
        if len(sub) > 1:
            raise Exception("Multiple subscription in pending , please contact support")
        if len(sub) == 1:
            return sub[0]
    


    def check_subscription_renewal_eligibility(self,lob_uid,plan_id):
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
            

    def create_payment_order(self,subscription_uid,receipt_id,payable_amount,payment_id,order_id,signature,status):
        with self.uow:
            sub = self.uow.subscription.get(id=subscription_uid, status='Pending')
            if not sub:
                raise Exception("Not a vaild subscription for payment")
                payment=SubscriptionPaymentOrder(
                                    uid=str(id),
                                    subscription_uid=subscription_uid,
                                    receipt_id=receipt_id,
                                    payable_amount=payable_amount,
                                    payment_id=payment_id, 
                                    order_id=order_id,
                                    signature=signature,
                                    status='Pending Payment',
                                    created_date=created)
                self.uow.payment.add(payment)
                self.uow.commit()
        return sub 

    def get_payment_order_by_receipt(self,receipt_id):
        with self.uow:
            order = self.uow.payment.get(id=receipt_id)
            if not order:
                raise Exception("Not a vaild order ")
        return order 

    def payment_verifed_start_subscription(self):
        
        pass

    def retrieve_subscription_history(self):
        pass

    def list_active_subscriptions(self):
        pass


    def retrieve_expired_subscriptions(self):
        pass


'''
    create_subscription_order

    update_subscription_payment_status

    get_subscription_order_by_id

    retrieve_subscription_history

    retrieve_subscription_history_for_lob

    pause_subscription

    list_cancelled_subscription

    list_active_subscriptions

    

    retrieve_expired_subscriptions


    def create_subscription(self, plan: Plans) -> SubscriptionOrders:
        subscription_uid = uuid.uuid4()
        subscription = SubscriptionOrders(uid=subscription_uid, plan_id=plan.uid, status=SubscriptionStatus.active)
        self.subscriptions_db[subscription_uid] = subscription
        return subscription

    def renew_subscription(self, subscription: SubscriptionOrders) -> SubscriptionOrders:
        renewal_period = timedelta(days=30)  # Example renewal period
        # Simulate creating a new subscription order record for renewal
        renewed_subscription = SubscriptionOrders(
            uid=uuid.uuid4(),
            plan_id=subscription.plan_id,
            status=SubscriptionStatus.active,
        )
        self.subscriptions_db[renewed_subscription.uid] = renewed_subscription
        return renewed_subscription

    def cancel_subscription(self, subscription: SubscriptionOrders) -> SubscriptionOrders:
        subscription.status = SubscriptionStatus.inactive
        return subscription

    def list_active_subscriptions(self) -> list[SubscriptionOrders]:
        active_subscriptions = [
            subscription for subscription in self.subscriptions_db.values()
            if subscription.status == SubscriptionStatus.active
        ]
        return active_subscriptions

    def check_subscription_renewal_eligibility(self, subscription: SubscriptionOrders) -> bool:
        renewal_threshold = timedelta(days=7)  # Example threshold before renewal
        return datetime.utcnow() + renewal_threshold >= subscription.created_date

    def calculate_next_renewal_date(self, subscription: SubscriptionOrders) -> datetime:
        renewal_period = timedelta(days=30)  # Example renewal period
        return subscription.created_date + renewal_period

    def update_subscription_payment_status(self, subscription: SubscriptionOrders, payment_id: str, paid_amount: float) -> SubscriptionOrders:
        subscription.payment_id = payment_id
        subscription.paid_amount = paid_amount
        return subscription

    def update_subscription_details(self, subscription: SubscriptionOrders, plan: Plans) -> SubscriptionOrders:
        subscription.plan_id = plan.uid
        return subscription

    def send_subscription_renewal_notification(self, subscription: SubscriptionOrders) -> None:
        print(f"Notification sent for subscription renewal: {subscription.uid}")

    def handle_failed_renewal(self, subscription: SubscriptionOrders) -> SubscriptionOrders:
        subscription.status = SubscriptionStatus.pending
        return subscription

    def retrieve_subscription_history(self, user_uid: uuid.UUID) -> list[SubscriptionOrders]:
        user_subscriptions = [
            subscription for subscription in self.subscriptions_db.values()
            if subscription.initiated_user_uid == user_uid
        ]
        return user_subscriptions

    def calculate_subscription_duration(self, subscription: SubscriptionOrders) -> timedelta:
        return datetime.utcnow() - subscription.created_date

    def has_subscription_expired(self, subscription: SubscriptionOrders) -> bool:
        return datetime.utcnow() > subscription.created_date

    def handle_subscription_upgrade_downgrade(self, subscription: SubscriptionOrders, new_plan: Plans) -> SubscriptionOrders:
        subscription.plan_id = new_plan.uid
        return subscription

    def validate_plan_availability(self, plan: Plans) -> bool:
        return plan.uid in self.plans_db

    def handle_subscription_pause_hold(self, subscription: SubscriptionOrders) -> SubscriptionOrders:
        subscription.status = SubscriptionStatus.inactive
        return subscription

    def retrieve_expired_subscriptions(self) -> list[SubscriptionOrders]:
        expired_subscriptions = [
            subscription for subscription in self.subscriptions_db.values()
            if subscription.status == SubscriptionStatus.inactive
        ]
        return expired_subscriptions
'''
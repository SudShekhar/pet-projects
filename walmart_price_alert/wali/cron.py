from django_cron import CronJobBase, Schedule
from wali.models import Discount, Product
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils import timezone

class RollbackFeedsCronJob(CronJobBase):
    RUN_AT_TIMES = ['00:00'] # every 2 hours
    RETRY_AFTER_FAILURE_MINS = 5
    schedule = Schedule(run_at_times=RUN_AT_TIMES,retry_after_failure_mins = RETRY_AFTER_FAILURE_MINS)
    code = 'wali.rollback'    # a unique code

    def do(self):
        from alert_rollbacks import MultipleSpecialFeeds
        mailer = MultipleSpecialFeeds("rollback","electronics")
        mailer.process()

class ManageDiscountsCron(CronJobBase):
    RUN_EVERY_MINS = 60
    RETRY_AFTER_FAILURE_MINS = 5
    schedule = Schedule(run_every_mins= RUN_EVERY_MINS,retry_after_failure_mins = RETRY_AFTER_FAILURE_MINS)
    code = 'wali.manage_discounts'    # a unique code

    def do(self):
        from manage_discounts import ManageDiscount
        m = ManageDiscount()
        m.run()

class SpecialBuyFeedsCronJob(CronJobBase):
    RUN_AT_TIMES = ['00:30'] # every 2 hours

    RETRY_AFTER_FAILURE_MINS = 5
    schedule = Schedule(run_at_times=RUN_AT_TIMES,retry_after_failure_mins = RETRY_AFTER_FAILURE_MINS)
    code = 'wali.special_buy'    # a unique code

    def do(self):
        from alert_rollbacks import MultipleSpecialFeeds
        mailer = MultipleSpecialFeeds("special_buy","electronics")
        mailer.process()

class ClearanceFeedsCronJob(CronJobBase):
    RUN_AT_TIMES = ['01:00'] # every 2 hours

    RETRY_AFTER_FAILURE_MINS = 5
    schedule = Schedule(run_at_times=RUN_AT_TIMES,retry_after_failure_mins = RETRY_AFTER_FAILURE_MINS)
    code = 'wali.clearance'    # a unique code

    def do(self):
        from alert_rollbacks import MultipleSpecialFeeds
        mailer = MultipleSpecialFeeds("rollback","electronics")
        mailer.process()

class ValuedayFeedsCronJob(CronJobBase):
    RUN_AT_TIMES = ['01:30'] # every 2 hours
    RETRY_AFTER_FAILURE_MINS = 5
    schedule = Schedule(run_at_times = RUN_AT_TIMES, retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'wali.Valueday'    # a unique code

    def do(self):
        from alert_rollbacks import SingleSpecialFeeds
        mailer = SingleSpecialFeeds("vod")
        mailer.process()

class ValuehourFeedsCronJob(CronJobBase):
    RUN_EVERY_MINS = 60 # every 2 hours
    RETRY_AFTER_FAILURE_MINS = 5
    schedule = Schedule(run_every_mins = RUN_EVERY_MINS, retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'wali.Valuehour'    # a unique code

    def do(self):
        from alert_rollbacks import SingleSpecialFeeds
        mailer = SingleSpecialFeeds("voh")
        #mailer.process()


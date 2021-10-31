from typing import List

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.utils.executor import Executor


class Scheduler(object):
    scheduler: AsyncIOScheduler = None

    @staticmethod
    def init(scheduler):
        Scheduler.scheduler = scheduler

    @staticmethod
    def configure(**kwargs):
        Scheduler.scheduler.configure(**kwargs)

    @staticmethod
    def start():
        Scheduler.scheduler.start()

    @staticmethod
    def add_test_plan(plan_id, plan_name, cron):
        return Scheduler.scheduler.add_job(func=Executor.run_test_plan, args=(plan_id,),
                                           name=plan_name, id=str(plan_id),
                                           trigger=CronTrigger.from_crontab(cron))

    @staticmethod
    def edit_test_plan(plan_id, plan_name, cron):
        Scheduler.scheduler.modify_job(job_id=str(plan_id), trigger=CronTrigger.from_crontab(cron), name=plan_name)

    @staticmethod
    def pause_resume_test_plan(plan_id, status):
        if status:
            Scheduler.scheduler.resume_job(job_id=str(plan_id))
        else:
            Scheduler.scheduler.pause_job(job_id=str(plan_id))

    @staticmethod
    def remove(plan_id):
        Scheduler.scheduler.remove_job(str(plan_id))

    @staticmethod
    def list_test_plan(data: List):
        for d in data:
            job = Scheduler.scheduler.get_job(str(d.get('id')))
            d["next_run"] = job.next_run_time

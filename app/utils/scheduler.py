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
        """
        通过测试计划id，更新测试计划任务的cron，name等数据
        :param plan_id:
        :param plan_name:
        :param cron:
        :return:
        """
        Scheduler.scheduler.modify_job(job_id=str(plan_id), trigger=CronTrigger.from_crontab(cron), name=plan_name)
        Scheduler.scheduler.pause_job(str(plan_id))
        Scheduler.scheduler.resume_job(str(plan_id))

    @staticmethod
    def pause_resume_test_plan(plan_id, status):
        """
        暂停或恢复测试计划，会影响到next_run_at
        :param plan_id:
        :param status:
        :return:
        """
        if status:
            Scheduler.scheduler.resume_job(job_id=str(plan_id))
        else:
            Scheduler.scheduler.pause_job(job_id=str(plan_id))

    @staticmethod
    def remove(plan_id):
        """
        删除job，当删除测试计划时，调用此方法
        :param plan_id:
        :return:
        """
        Scheduler.scheduler.remove_job(str(plan_id))

    @staticmethod
    def list_test_plan(data: List):
        for d in data:
            job = Scheduler.scheduler.get_job(str(d.get('id')))
            if job is None:
                # 说明job初始化失败了
                d["state"] = 2
                continue
            if job.next_run_time is None:
                # 说明job被暂停了
                d["state"] = 3
            else:
                d["next_run"] = job.next_run_time.strftime("%Y-%m-%d %H:%M:%S")

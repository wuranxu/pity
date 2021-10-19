from apscheduler.schedulers.asyncio import AsyncIOScheduler


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
    def add():
        # Scheduler.scheduler.add_job(id=job_id, func=print_time, args=(job_id,), trigger=CronTrigger.from_crontab(cron))
        pass

    @staticmethod
    def edit():
        pass

    @staticmethod
    def remove():
        pass

    @staticmethod
    def list():
        pass

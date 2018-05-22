# -*- coding: utf-8 -*-
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler


sched = BlockingScheduler()

@sched.scheduled_job('interval',id="testkuaidaili_query", seconds=5)
def kuaidaili_query():
    job = sched.get_job(job_id="testkuaidaili_query")
    next = int(job.next_run_time.strftime('%Y%m%d%H%M%S'))

    print(next)
    while True:
        now = int(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        if next-now<2:
            print("结束")
            return

    pass



if __name__ == '__main__':
    print("sched.start()")
    sched.start()
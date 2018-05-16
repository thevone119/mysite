import time
from apscheduler.schedulers.blocking import BlockingScheduler

#interval 间隔调度



sched = BlockingScheduler()


#每5秒执行一次
@sched.scheduled_job('interval', seconds=5,max_instances=2)
def my_job():
    print("my_job")
    print(time.time())
    time.sleep(11)



#每5分钟执行一次
@sched.scheduled_job('interval', minutes=5)
def my_job2():
    pass
    #print("my_job2")
    #print(time.time())



sched.start()
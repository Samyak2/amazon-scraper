import subprocess
def start_scraper():
    subprocess.Popen(["scrapy", "crawl", "amazon_spider", "-o", "output.json"])

# All the required imports
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.combining import OrTrigger
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler

def start_scheduler():

     # define a background schedule 
     # Attention: you cannot use a blocking scheduler here as that will block the script from proceeding.
     scheduler = BlockingScheduler()

     # define your job trigger
     hourse_keeping_trigger = CronTrigger(hour="*/3") #OrTrigger([CronTrigger()]) #CronTrigger(hour='12', minute='30')

     # add your job
     scheduler.add_job(func=start_scraper, trigger=hourse_keeping_trigger)

     # start the scheduler
     scheduler.start()


def run():
    start_scheduler()

if __name__ == '__main__':
    run()
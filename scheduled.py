from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess

sched = BlockingScheduler()

@sched.scheduled_job('interval', hours=3)
def timed_job():
    subprocess.Popen(["scrapy", "crawl", "amazon_spider", "-o", "output.json"])

sched.start()
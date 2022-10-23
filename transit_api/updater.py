from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
from .update.line_update import update_line_info
from .update.stop_update import update_stop_info
from .update.train_update import update_train_info

UPDATE_INTERVAL_STOP =  86400 # daily
UPDATE_INTERVAL_LINE = 86400 # daily
UPDATE_INTERVAL_TRAIN =  15 # 15 seconds

UPDATE_LINE_INFO_LAST_MOD = None
UDPATE_STOP_INFO_LAST_MOD = None
UPDATE_TRAIN_INFO_LAST_MOD1 = None 
UPDATE_TRAIN_INFO_LAST_MOD2 = None

def start():
    def transit_listener(event):
        if not event.exception:
            job = scheduler.get_job(event.job_id)
            print(job.name)
            if (job.name == 'update_line_info'):
                global UPDATE_LINE_INFO_LAST_MOD
                last_modified = update_line_info(UPDATE_LINE_INFO_LAST_MOD)
                UPDATE_LINE_INFO_LAST_MOD = last_modified
            if (job.name == 'update_stop_info'):
                global UDPATE_STOP_INFO_LAST_MOD
                last_modified = update_stop_info(UDPATE_STOP_INFO_LAST_MOD)
                UDPATE_STOP_INFO_LAST_MOD = last_modified
            if (job.name == 'update_train_info'):
                global UPDATE_TRAIN_INFO_LAST_MOD1
                global UPDATE_TRAIN_INFO_LAST_MOD2
                last_modified1, last_modified2 = update_train_info(UPDATE_TRAIN_INFO_LAST_MOD1, UPDATE_TRAIN_INFO_LAST_MOD2)
                UPDATE_TRAIN_INFO_LAST_MOD1, UPDATE_TRAIN_INFO_LAST_MOD2 = last_modified1, last_modified2

    scheduler = BackgroundScheduler(job_defaults={"max_instances": 20})
    scheduler.add_listener(transit_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    scheduler.add_job(update_line_info, 'interval', args=[UPDATE_LINE_INFO_LAST_MOD], seconds=UPDATE_INTERVAL_LINE)
    scheduler.add_job(update_stop_info, 'interval', args=[UDPATE_STOP_INFO_LAST_MOD], seconds=UPDATE_INTERVAL_STOP)
    scheduler.add_job(update_train_info, 'interval', args=[UPDATE_TRAIN_INFO_LAST_MOD1, UPDATE_TRAIN_INFO_LAST_MOD2], seconds=UPDATE_INTERVAL_TRAIN)
    scheduler.start()


        
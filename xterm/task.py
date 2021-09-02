from celery import shared_task
from celery.utils.log import get_task_logger
import docker

import time
logger = get_task_logger(__name__)


@shared_task(bind=True)
def add (self,x,y):
    print("adding")
    self.update_state(
        state="pending",
        meta={
            'current': "1",
            'total': "10",
        }
    )
    time.sleep(3)
    self.update_state(
        state="finished",
        meta={
            'current': "2",
            'total': "10",
        }
    )
    
    return x+y
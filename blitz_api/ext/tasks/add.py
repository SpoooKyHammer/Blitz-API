
import time

from celery import shared_task

@shared_task(ignore_result=False)
def add(n,m) -> int:
    time.sleep(10)
    return n+m

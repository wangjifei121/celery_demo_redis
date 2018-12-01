import time
import random
from celery import Celery

# 创建celery对象
app = Celery('tasks', broker='redis://127.0.0.1:6379', backend='redis://127.0.0.1:6379')

# 创建任务
@app.task
def create_order(gid):
    time.sleep(10)
    v = random.randint(1,4)
    if v == 2:
        return '抢购成功'
    else:
        return '抢购失败'

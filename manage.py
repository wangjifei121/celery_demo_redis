from flask import Flask, render_template, request
from celery.result import AsyncResult # 异步获取结果
from celery_task import create_order # 导入任务
from celery_task import app as celery_app # 导入celery对象

#实例化flask对象
app = Flask(__name__)

GOODS_LIST = [
    {'id': 1, 'title': '小米手机'},
    {'id': 2, 'title': '小米手环'},
    {'id': 3, 'title': '小米电视'},
]

@app.route('/goods')
def goods():
    return render_template('goods.html', gds=GOODS_LIST)


@app.route('/buy')
def buy():
    gid = request.args.get('gid') # 获取前端用户要购买的商品id
    result = create_order.delay(gid) #执行抢购任务
    return render_template('tips.html', task_id=result.id)


@app.route('/check')
def check():
    task_id = request.args.get('task') #获得参数
    async = AsyncResult(id=task_id, app=celery_app)#查看任务结果
    if async.successful():
        result = async.get()# 获取任务结果
        return result
    else:
        return '还在排队等待中'


if __name__ == '__main__':
    app.run()

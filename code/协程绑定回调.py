import asyncio


async def request(url):
    print('正在请求 '+url)
    print('下载成功')


# 回调函数必须有一个参数:task
# task.result():任务对象封装的协程对象对应的特殊函数内部的返回值
def callback(task):
    print('callback')
    print(task.result())


c = request('www.baidu.com')
# 给任务对象绑定回调函数
task = asyncio.ensure_future(c)
task.add_done_callback(callback)
loop = asyncio.get_event_loop()
loop.run_until_complete(task)

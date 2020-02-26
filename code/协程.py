import asyncio


async def request(url):
    print('正在请求 '+url)
    print('下载成功')
c = request('www.baidu.com')
# 实例化一个事件循环对象
loop = asyncio.get_event_loop()
# 创建一个任务对象，将协程对象封装到该对象中
# task = asyncio.create_task(c)
# 另一种方式创建任务对象
task = asyncio.ensure_future(c)
print(task)
# 将任务对象注册到循环对象中，并启动事件循环对象
loop.run_until_complete(task)
print(task)
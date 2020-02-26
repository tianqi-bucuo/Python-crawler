import asyncio
import time

urls = ['www.baidu.com', 'www.sougou.com', 'www.huohu.com']
start = time.time()


async def request(url):
    print('正在请求：', url)
    # 在多任务异步协程实现中，不可以出现不支持异步的相关代码(time.sleep())
    # time.sleep(2)
    await asyncio.sleep(2)
    print('下载成功', url)
# loop的作用：可以将多个任务对象注册到loop中，
# loop就可以通过不间断循环的方式异步执行任务对象
loop = asyncio.get_event_loop()
# 任务列表放置多个任务对象
tasks = []
for url in urls:
    c = request(url)
    task = asyncio.ensure_future(c)
    tasks.append(task)
loop.run_until_complete(asyncio.wait(tasks))
print(time.time()-start)

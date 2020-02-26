import aiohttp
import asyncio


async def request(url):
    async with aiohttp.ClientSession() as s:
        async with await s.get(url=url) as response:
            page_text = await response.text()
            return page_text


def callback1(task):
    print(task.result())


def callback2(task):
    print(task.result())


# 事件循环对象
loop = asyncio.get_event_loop()
c1 = request('https://www.baidu.com/')
c2 = request('http://www.sougou.com/')

task1 = asyncio.ensure_future(c1)
task1.add_done_callback(callback1)
task2 = asyncio.ensure_future(c2)
task2.add_done_callback(callback2)

tasks = [task1, task2]
loop.run_until_complete(asyncio.wait(tasks))
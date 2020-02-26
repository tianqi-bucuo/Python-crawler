# selenium的使用必须在有浏览器环境的情况下
# pyppeteer自动安装chromium浏览器，不需要原有的浏览器环境
from pyppeteer import launch
from lxml import etree
import asyncio


async def main():
    # 实例化一个浏览器对象(谷歌浏览器测试版本)
    bro = await launch(headless=False)
    # 新建一个空白页
    page = await bro.newPage()
    await page.goto('http://quotes.toscrape.com/js/')

    page_text = await page.content()
    return page_text


def parse(task):
    page_text = task.result()
    tree = etree.HTML(page_text)
    div_list = tree.xpath('//div[@class="quote"]')
    for div in div_list:
        content = div.xpath('./span[1]/text()')[0]
        print(content)


c = main()
task = asyncio.ensure_future(c)
task.add_done_callback(parse)
loop = asyncio.get_event_loop()
loop.run_until_complete(task)
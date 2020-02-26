from selenium import webdriver
from lxml import etree
import time

# 实例化一个浏览器对象，executable_table是chromedrive的路径
bro = webdriver.Chrome(executable_path='chromedriver.exe')
# 让浏览器对指定url发起访问
bro.get('http://125.35.6.84:81/xk/')
# 获取页面源码(可见即可得)
page_text = bro.page_source
tree = etree.HTML(page_text)
# 可以获取动态加载的数据
name = tree.xpath('//*[@id="gzlist"]/li[1]/dl/a/text()')[0]
print(name)
time.sleep(2)
bro.quit()
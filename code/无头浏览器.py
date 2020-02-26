# 浏览器不可见
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lxml import etree
import time

chrome_options = Options()
# 设置不可见
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
bro = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)
# 让浏览器对指定url发起访问
bro.get('http://125.35.6.84:81/xk/')
# 获取页面源码(可见即可得)
page_text = bro.page_source
time.sleep(2)
tree = etree.HTML(page_text)
# 可以获取动态加载的数据
name = tree.xpath('//*[@id="gzlist"]/li[1]/dl/a/text()')[0]
print(name)
time.sleep(2)
bro.quit()

from selenium import webdriver
from lxml import etree
from selenium.webdriver import ChromeOptions
import time

# 用来规避检测
option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])
bro = webdriver.Chrome(executable_path='chromedriver.exe', options=option)
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
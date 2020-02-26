from selenium import webdriver
import time

bro = webdriver.Chrome(executable_path='chromedriver.exe')
bro.get('https://www.taobao.com')
# 标签定位:find系列方法
input_text = bro.find_element_by_id('q')
input_text.send_keys('mac')
time.sleep(2)
# 执行js程序
bro.execute_script('window.scrollTo(0,document.body.scrollHeight)')
btn = bro.find_element_by_css_selector('.btn-search')
btn.click()
time.sleep(3)
bro.quit()

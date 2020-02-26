from selenium import webdriver
from selenium.webdriver import ActionChains
import time

bro = webdriver.Chrome(executable_path='chromedriver.exe')
bro.get('https://www.runoob.com/try/try.php?filename=jqueryui-api-droppable')
# 如果定位的标签是被包含在iframe标签中，使用switch_to进行frame的切换
bro.switch_to.frame('iframeResult')
div_tag = bro.find_element_by_id('draggable')
# 实例化一个动作链对象,并将浏览器对象传递给它
act = ActionChains(bro)
# 单击且长按
act.click_and_hold(div_tag)
# 让div向右移动
for i in range(5):
    act.move_by_offset(17, 0).perform()  # perform立即执行动作链
    time.sleep(0.2)
print(div_tag)
time.sleep(2)
bro.quit()
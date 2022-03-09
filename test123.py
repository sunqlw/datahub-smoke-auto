from selenium import webdriver
import time
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

driver = webdriver.Chrome()
driver.get('http://demo29.test.com:4019/datahub')
driver.maximize_window()
time.sleep(1)
elem = driver.find_element_by_xpath('//ul[@class="main-nav"]/li[2]/div')
try:
    style_red = 'arguments[0].style.border="2px solid #FF0000"'
    style_blue = 'arguments[0].style.border="2px solid #00FF00"'
    style_null = 'arguments[0].style.border=""'

    for _ in range(2):
        driver.execute_script(style_red, elem)
        time.sleep(0.1)
        driver.execute_script(style_blue, elem)
        time.sleep(0.1)
    driver.execute_script(style_blue, elem)
    time.sleep(0.5)
    driver.execute_script(style_null, elem)
except WebDriverException:
    pass
time.sleep(2)
elem.click()
elem = driver.find_element_by_xpath('//i[@title="删除"]')
time.sleep(4)
elem.click()
# ele = driver.find_element_by_class_name('el-message-box')
# driver.find_element_by_xpath('//div[@class="el-message-box__btns"]/button[1]').click()
# WebDriverWait(driver, 1).until_not(ec.visibility_of(elem), '元素未消失')
time.sleep(2)
driver.quit()

#实现自动化登录微博
from selenium import webdriver
from time import sleep
import selenium
dr = webdriver.Chrome()
dr.get("http://weibo.com/login.php")
dr.find_element_by_id("loginname").send_keys("username")
dr.find_element_by_name("password").send_keys("user_password")
dr.find_element_by_class_name('W_btn_a').click()
sleep(5)
dr.get_screenshot_as_file("F:\\weibo_ok.jpg")
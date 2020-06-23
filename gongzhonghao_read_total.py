# coding: utf-8
from selenium import webdriver
import re
import time
import pickle
import csv
from selenium.common.exceptions import TimeoutException

"""
note: 需要使用selenium，chrome版本需要与chromedriver版本对应。具体见https://chromedriver.storage.googleapis.com/
"""

def login(username, password):
    #打开微信公众号登录页面
    driver.get('https://mp.weixin.qq.com/')
    driver.maximize_window()
    time.sleep(3)
    driver.find_element_by_xpath("//*[@id=\"header\"]/div[2]/div/div/div[2]/a").click()
    # 自动填充帐号密码
    driver.find_element_by_xpath("//*[@id=\"header\"]/div[2]/div/div/div[1]/form/div[1]/div[1]/div/span/input").clear()
    driver.find_element_by_xpath("//*[@id=\"header\"]/div[2]/div/div/div[1]/form/div[1]/div[1]/div/span/input").send_keys(username)
    driver.find_element_by_xpath("//*[@id=\"header\"]/div[2]/div/div/div[1]/form/div[1]/div[2]/div/span/input").clear()
    driver.find_element_by_xpath("//*[@id=\"header\"]/div[2]/div/div/div[1]/form/div[1]/div[2]/div/span/input").send_keys(password)

    time.sleep(1)
    #自动点击登录按钮进行登录
    driver.find_element_by_xpath("//*[@id=\"header\"]/div[2]/div/div/div[1]/form/div[4]/a").click()
    # 手动拿手机扫二维码！
    time.sleep(15)

"""定义获得送达人数和阅读数，生成带字典的数组"""


def get_postnum_readnum(html):
    lst = []

    for i in range(1, 8):
            try:
                driver.find_element_by_xpath("//*[@id=\"list\"]/li[{0}]/div[1]/div[1]".format(i)).click()
                temp_dict = {
                    'postnum': driver.find_element_by_xpath("//*[@id=\"list\"]/li[{0}]/div[1]/div[1]/span/div/div/div[2]/p[1]/span".format(i)).text,
                    'readnum': driver.find_element_by_xpath('//*[@id=\"list\"]/li[{0}]/div[2]/span/div/div[2]/div/div[1]/div/span'.format(i)).text,
                    'title': driver.find_element_by_xpath(
                        '//*[@id="list"]/li[{0}]/div[2]/span/div/div[2]/a/span'.format(i)).get_attribute(
                        'textContent'),
                    'date': driver.find_element_by_xpath("//*[@id=\"list\"]/li[{0}]/div[1]/em".format(i)).text,
                }
                driver.find_element_by_xpath("//*[@id=\"list_container\"]/div[1]/div[2]/div/span/input").click()
                lst.append(temp_dict)
            except:
                driver.find_element_by_xpath("//*[@id=\"list_container\"]/div[1]/div[2]/div/span/input").click()
                continue

    return lst



#用webdriver启动谷歌浏览器
chrome_driver = r"C:\Users\jiansi\PycharmProjects\jiansidata\venv\Lib\site-packages\selenium\webdriver\chrome\chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver)

"""需要手动输入个人微信公众号的账号，密码，要导出的公众号名称"""
username = '' # 账号
password = '' # 密码
login(username, password)
page_num = int(driver.find_elements_by_class_name('weui-desktop-pagination__num__wrp')[-1].text.split('/')[-1])
# 点击下一页
num_lst = get_postnum_readnum(driver.page_source)
#print(num_lst)
for _ in range(1, page_num):
        try:
            pagination = driver.find_elements_by_class_name('weui-desktop-pagination__nav')[-1]
            pagination.find_elements_by_tag_name('a')[-1].click()
            time.sleep(5)
            num_lst += get_postnum_readnum(driver.page_source)

        except:
            continue


print(num_lst)
with open('1.csv', 'w', encoding="utf-8", newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['postnum', 'readnum', 'title', 'date'])
    writer.writeheader()
    writer.writerows(num_lst)


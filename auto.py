#coding: utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
import time
import csv
from collections import Iterable

class REMAPPING():
    Name = 0,
    Email = 1,

    Billing_Name = 24,
    Billing_Street = 25,
    Billing_Address1 = 26,
    Billing_Address2 = 27,
    Billing_Company = 28,
    Billing_City = 29,
    Billing_Zip = 30,
    Billing_Province = 31,
    Billing_Country = 32,
    Billing_Phone = 33,


class AutoFill:
    def __init__(self, login_name, login_password):
        #self.driver = webdriver.Chrome(r"/usr/local/bin/chromedriver")
        self.base_url = "http://portal.yw56.com.cn/login"
        self.login_name = login_name
        self.login_password = login_password
        self.data_reader = None
        self.data_iterator = 1
        self.file_name = ""

    def parse_file(self, filepath):
        fp = open(filepath)
        self.file_name = os.path.basename(filepath)
        self.data_iterator = iter(csv.reader(fp))

    def next_run(self):
        items = None
        try:
            items = next(self.data_iterator)
        except StopIteration:
            return

        data = {
            "ContentPlaceHolder1_txtUserOrderNum": items[REMAPPING.Name],  # A
            "ContentPlaceHolder1_txtName": items[REMAPPING.Billing_Name],  # Y
            "ContentPlaceHolder1_txtPhone": items[REMAPPING.Billing_Phone],
            "ContentPlaceHolder1_txtCountry": items[REMAPPING.Billing_Country],  # AG
            "ContentPlaceHolder1_txtPostCode": items[REMAPPING.Billing_Zip],  # AE
            "ContentPlaceHolder1_txtState": "south",  # AF
            "ContentPlaceHolder1_txtCity": "jingsu",  # AD
            "ContentPlaceHolder1_txtAddress1": "yuhuaqu",  # Z
            "ContentPlaceHolder1_txtNameCh": u"你好",
            "ContentPlaceHolder1_txtNameEn": "Hello",
            "ContentPlaceHolder1_txtWeight": "123",
            "ContentPlaceHolder1_txtDeclaredValue": "$100"
        }

    def login(self):
        self.driver.get(self.base_url)

        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "login_btn")))
        self.driver.find_element_by_name("loginName").send_keys(self.login_name)
        self.driver.find_element_by_name("password").send_keys(self.login_password)
        self.driver.find_element_by_id("login_btn").click()

        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "进入EJF"))).click()

    def fill_order(self, data):
        time.sleep(1)
        self.driver.switch_to.window(self.driver.window_handles[-1])
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "新建快件信息"))).click()

        self.driver.switch_to.window(self.driver.window_handles[-1])
        data = {
            "ContentPlaceHolder1_txtUserOrderNum": "12345", #A
            "ContentPlaceHolder1_txtName": "Neil", #Y
            "ContentPlaceHolder1_txtPhone": "123057531957",
            "ContentPlaceHolder1_txtCountry": "China", #AG
            "ContentPlaceHolder1_txtPostCode": "12345", #AE
            "ContentPlaceHolder1_txtState": "south", #AF
            "ContentPlaceHolder1_txtCity": "jingsu", #AD
            "ContentPlaceHolder1_txtAddress1": "yuhuaqu", #Z
            "ContentPlaceHolder1_txtNameCh": u"你好",
            "ContentPlaceHolder1_txtNameEn": "Hello",
            "ContentPlaceHolder1_txtWeight": "123",
            "ContentPlaceHolder1_txtDeclaredValue": "$100"
        }

        #发货方式
        self.driver.find_element_by_id("ContentPlaceHolder1_ctrlChannel").click()
        self.driver.find_element_by_xpath('//option[@value="662"]').click()

        for id in data:
            try:
                element = self.driver.find_element_by_id(id)
                element.clear()
                element.send_keys(data[id])
            except Exception as e:
                print e



a = AutoFill("13401924592", "trendmicro")
a.parse_file("/Users/mac/PycharmProjects/AutoFill/form_tool/T恤-Tshirt.csv")
for i in range(1000):
    a.next_run()
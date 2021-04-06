""""
使用前请仔细阅读README文件！涉及到个人隐私问题，希望使用者知道自己在干什么。
如果不想涉及隐私问题，可向别人借研招网账号查询，但是无法查看自己是否能申请(如果别人的专业和自己不一样，一样则可以)
"""

## crawl part
from selenium import webdriver
import random
import pandas as pd
from time import sleep
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service

import os
import datetime
import sys

#email part
from set_up_email import set_up_email,send_email,get_html_msg

# needed webdriver path
def set_up_selenium(webdriver_path,chrome_options):
    return webdriver.Chrome(webdriver_path,options=chrome_options)

# set up your personnal info ,like your account
def set_up_login(username,password,driver):
    """
    启动driver到研招网页面并输入登录信息
    """
    driver.get("https://yz.chsi.com.cn/sytj/tj/qecx.html")
    input_username = driver.find_element_by_id("username")
    input_password = driver.find_element_by_id("password")
    input_username.send_keys(username)
    input_password.send_keys(password)
    login_button =  driver.find_element_by_name("submit")
    login_button.click()

# 
def check_major(driver,major):
    # 跳转到余额查询页面
    continue_link = driver.find_element_by_link_text('计划余额查询')
    continue_link.click()
    #跳转到模糊查询
    sleep(3)
    switch_search = driver.find_element_by_xpath("//*[@id='tj_seach_change']/div/div/ul/li[2]")
    switch_search.click()
    #模拟输入想要查询的专业
    major_input = driver.find_element_by_id("dwxx")
    major_input.send_keys(major)
    submit_button = driver.find_element_by_xpath("//*[@id='tj_seach_form']/table/tbody/tr/td[6]/a")
    submit_button.click()


# 选择地区和学习方式
def select(driver,loc="不限",study="不限"):
    # 地区
    select = Select(driver.find_element_by_id('ss'))
    options = [i.text for i  in select.options]
    loc = [locs for locs in options if loc in locs] #比如“北京” 获得“(11) 北京”

    select.select_by_visible_text(loc[0])
    # 全日制或 非全
    study_way = Select(driver.find_element_by_id('xxfs'))
    study_way.select_by_visible_text(study)

def get_data(driver):
    print("----Now Working Geting Data------")
    html = driver.page_source #获得当前页面的html
    
    try:
        df = pd.read_html(html)[1] #html里有两个table，第二个是我们需要的
    except:#并释放driver资源
        print("Can Not read_html ,save html for next debug!")
        with open("debug.html",mode="w") as fd:
            fd.write(html)
        print("GET debug_html! ERROR return!")
        driver.quit()
        return pd.DataFrame()
    
    page = driver.find_elements_by_class_name("tj-paging-item") #获取页数
    page_len = len(page) -3 # two for switch ，one for current page
    print(page_len)
    #遍历所有页面，收集数据
    for i in range(page_len):
        sleep(random.randint(5,7))
        driver.find_element_by_link_text("下一页").click() #点击下一页
        current_html = driver.page_source
        current_df = pd.read_html(current_html)[1] # two table in html
        df = df.append(current_df) #将每一个页面的数据都加到df里面
    driver.quit()
    print("-------Getted All wanted Data return Back!---------")
    return df

#只查阅自己可以申请的院校信息
def apply_true(df):
    return df[df["操作"] == "申请"]

def compare(df,current_df):
    df["split"] = True
    current_df["split"]  = False
    df = df.append(current_df)
    df.drop_duplicates(subset = ['招生单位', '院系所', '专业', '研究方向', '学习方式'],keep=False,inplace=True)
    return df[df["split"] == True].drop(axis=1,columns=["split"])
if __name__ == "__main__":
    
    ### 设置区域
    webdriver_path = r"/usr/sbin/chromedriver"        #chromedriver路径
    username = ""   #研招网账号
    password = ""   #密码
    major = ""          #想要查询的专业
    loc = ""                #想要查询的地区 如北京、广东等一定要和研招网上可以选的地区一致
    study =""               #学习方式 ： “不限” “全日制” “非全日制”  
    apply_only = True          #只查看能申请的

    host_server = "smtp.qq.com"             #smtp host 非qq的话要修改
    sender_qq = ""
    pwd = ""                # qq邮箱授权码
    sender_email = ""  # qq邮箱
    receiver =  ""  #接受邮箱
    ## 启动part
    
    driver_service = Service(webdriver_path)   
    driver_service.command_line_args()
    driver_service.start()
    chrome_options = webdriver.ChromeOptions()

    #无界面模式  建议debug的时候把这行给注释掉
    chrome_options.add_argument('--headless')
    
    driver = set_up_selenium(webdriver_path,chrome_options)
    set_up_login(username,password,driver)
    check_major(driver,major)
    select(driver,loc,study)

    # 获取数据
    df = get_data(driver)
    ## ERROR control
    if df.empty == True:
        driver_service.stop()
        print("stop driver_service, exit for error html table ! BUG needed solve!")
        sys.exit(1)
    
    driver_service.stop()      #退出chromedriver
    
    if apply_only:
        df = apply_true(df)
        
    csv_name = "current_info.csv"
    if os.path.exists(csv_name):
        current_df = pd.read_csv(csv_name)
        drop_dup_df = compare(df,current_df)
        if len(drop_dup_df)>1:
            df.to_csv(csv_name) #保存数据到current.csv中
            ## 邮件设置
            mail_title = "您有更新的调剂信息需要查看"
            mail_content = get_html_msg(drop_dup_df)
            smtp = set_up_email(host_server,sender_qq,pwd)
            send_email(smtp,mail_title,mail_content,sender_email,receiver)
        else:
            print("Nothing to do!")
    else:
        df.to_csv(csv_name) #保存数据到current.csv中
        mail_title = "您的第一次调剂信息需要查看"
        mail_content = get_html_msg(df)
        smtp = set_up_email(host_server,sender_qq,pwd)
        send_email(smtp,mail_title,mail_content,sender_email,receiver)
    print("-------------PRINT TIME ---------------------")  
    print("Current Time is %s \n"%datetime.datetime.now())
    print("------------- Job Done -----------------------")
    sys.exit(0)
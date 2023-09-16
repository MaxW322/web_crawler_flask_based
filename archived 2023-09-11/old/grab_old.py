import time
import datetime
import pandas as pd
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from lxml import etree
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.page_load_strategy = 'normal'


def last_comment_date(html):
    root = etree.HTML(html)
    # root = etree.HTML(chrome.page_source)
    comment_list = root.xpath('//*[@id="list"]')
    for comment_l in comment_list:
        comment_date = comment_l.xpath(
            '//*[@id="list"]//*[@class=" "]//*[@class="basic_info"]/text()'
        )
        temp = comment_date[len(comment_date) - 1]
        temp = temp.replace("更新于 ", "")
        today = time.strftime("%m-%d", time.localtime())
        if "今天" in temp:
            temp = temp.replace("今天", f"{today}")
        last = temp[0:-6]
        # print(last)
        return last


def parse(html, _sheet):
    root = etree.HTML(html)
    # root = etree.HTML(chrome.page_source)
    comment_list = root.xpath('//*[@id="list"]')  # element对象
    items = {}
    for comment_l in comment_list:
        comment_text = comment_l.xpath(
            '//*[@id="list"]//*[@class=" "]//*[@class="content"]/a/span/text()[1]'
        )
        comment_date = comment_l.xpath(
            '//*[@id="list"]//*[@class=" "]//*[@class="basic_info"]/text()'
        )
        for comment_text_, comment_date_ in zip(comment_text, comment_date):
            # print(comment_text_, comment_date_)

            items["comment_text"] = comment_text_
            temp = comment_date_
            temp = temp.replace("更新于 ", "")
            today = time.strftime("%m-%d", time.localtime())
            if "今天" in comment_date_:
                temp = temp.replace("今天", f"{today}")
            items["comment_date"] = temp
            tt = pd.DataFrame(data=[comment_text_, temp, temp[0:-6]]).T
            tt.columns = ["comment_text", "comment_date", "comment_time"]
            _sheet = pd.concat((tt, _sheet))
    return _sheet


class grab:
    def __init__(self, code, day):
        self.data = pd.DataFrame(columns=["comment_text", "comment_date", "comment_time"])
        self.day = day
        self.code = code
        # self.chrome = Chrome(options=chrome_options)
        self.chrome = Chrome()
        print('Chrome初始化成功')
        self.open_main(f"https://guba.eastmoney.com/list,{self.code}.html?from=BaiduAladdin", self.day)
        self.data = self.data.sort_values(by=["comment_date"])
        self.data.to_csv(f"./output/data_{self.code}.csv", encoding="gbk", index_label=None)
        print(f'已输出爬取数据./output/data_{self.code}.csv')
        self.chrome.close()

    def open_main(self, url, day):
        # global last_day_, day_
        self.chrome.get(url)
        # time.sleep(5)
        # list_0 = chrome.find_element(By.XPATH, '//*[@id="mainlist"]/div/div[1]/div/ul/li[2]')
        list_1 = self.chrome.find_element(
            By.XPATH, '//*[@id="mainlist"]/div/div[1]/div/ul/li[3]'
        )
        # list_0.click()
        list_1.click()  # 点击摘要
        time.sleep(2)
        day_ = datetime.datetime.strptime(day, "%m-%d")

        last_day = last_comment_date(self.chrome.page_source)
        # print(last_day)

        last_day_ = datetime.datetime.strptime(last_day, "%m-%d")

        n = 1  # 初试页面 页号1
        while last_day_ >= day_:
            self.next_page()
            time.sleep(2)
            tt = parse(self.chrome.page_source, self.data)
            tt.columns = ["comment_text", "comment_date", "comment_time"]
            self.data = pd.concat((tt, self.data))
            last_day = last_comment_date(self.chrome.page_source)
            last_day_ = datetime.datetime.strptime(last_day, "%m-%d")
        #     n = n + 1
        #     if n==10:
        #         self.chrome.quit()
        #         self.chrome = Chrome()

        # n = 1  # 初试页面 页号1
        # c = 1
        # while last_day_ >= day_:
        #     if n == 1:
        #         self.chrome.get(f'https://guba.eastmoney.com/list,{self.code}.html')
        #     else:
        #         if c == 10:
        #             self.chrome.quit()
        #             self.chrome = Chrome()
        #             self.chrome.get(f'https://guba.eastmoney.com/list,{self.code}_{n}.html')
        #
        #             list_1 = self.chrome.find_element(
        #                 By.XPATH, '//*[@id="mainlist"]/div/div[1]/div/ul/li[3]'
        #             )
        #             # list_0.click()
        #             list_1.click()  # 点击摘要
        #             c = 1
        #             time.sleep(2)
        #         else:
        #             self.chrome.get(f'https://guba.eastmoney.com/list,{self.code}_{n}.html')
        #     # time.sleep(2)
        #     tt = parse(self.chrome.page_source, self.data)
        #     tt.columns = ["comment_text", "comment_date", "comment_time"]
        #     self.data = pd.concat((tt, self.data))
        #     last_day = last_comment_date(self.chrome.page_source)
        #     last_day_ = datetime.datetime.strptime(last_day, "%m-%d")
        #     # time.sleep(2)
        #     n = n + 1
        #     c = c + 1

    def next_page(self):
        next_button = self.chrome.find_element(By.CLASS_NAME, "nextp")
        next_page_link = next_button.get_attribute("href")
        self.chrome.get(next_page_link)
        # self.chrome.refresh()
        # self.chrome.execute_script(f'window.open("{next_page_link}", "_blank");')
        # self.chrome.close()
        # self.chrome = Edge()
        # self.chrome.get(next_page_link)
        # list_1 = self.chrome.find_element(
        #     By.XPATH, '//*[@id="mainlist"]/div/div[1]/div/ul/li[3]'
        # )
        # # list_0.click()
        # list_1.click()  # 点击摘要

    # def last_comment_date():
    #     comment_date_ = chrome.find_element(By.XPATH, '//*[@id="list"]//*[@class=" "]//*[@class="basic_info"]')
    #     comment_date = comment_date_.get_attribute('text')
    #     temp = comment_date[len(comment_date) - 1]
    #     temp = temp.replace('更新于 ', '')
    #     today = time.strftime('%m-%d', time.localtime())
    #     if '今天' in temp:
    #         temp = temp.replace('今天', f'{today}')
    #     last = temp[0:-6]
    #     return last

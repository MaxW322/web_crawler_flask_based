from selenium import webdriver
import time

from grab import grab_data

# def a():
#     b = webdriver.Chrome()
#     b.get('https://www.baidu.com/')
#     time.sleep(3)
#     b.quit()
#
#
# if __name__ == '__main__':
#     a()

# import pandas as pd
#
# data = pd.read_csv("./output/300059.csv", encoding="gbk", index_col=0)
# data = data.reset_index(drop=True)
# code = "300059"
# data.to_csv(f"./output/{code}.csv", encoding="gbk", index_label=None)

grab_data(code=300059, day='08-01')
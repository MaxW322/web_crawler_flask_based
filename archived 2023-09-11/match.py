import jieba
import pandas as pd

good_words = [
    "空",
    "利空",
    "收跌",
    "大跌",
    "暴跌",
    "收紧",
    "离场",
    "下跌",
    "看空",
    "看跌",
    "跌",
    "亏损",
    "亏钱",
    "亏了",
    "亏麻了",
    "割韭菜",
    "被割了",
    "套住",
    "被套",
    "深套",
    "砸盘",
    "砸",
    "主力离场",
    "主力抛售",
    "主力出货",
    "卖",
    "抛售",
    "出货",
    "杀跌",
    "流出",
    "空头",
    "跌停",
    "出手",
    "涨不起来",
    "做空",
    "回本之路",
    "大跌",
    "阴跌",
    "亏",
    "大阴线",
    "断崖式",
    "阴线",
    "没有未来",
    "死叉",
    "大减",
    "高开低走",
    "减持",
    "害死",
    "亏了",
    "垃圾",
    "输",
    "割肉",
]

bad_words = [
    "多",
    "利多",
    "利好",
    "收涨",
    "大涨",
    "暴涨",
    "开放",
    "增加",
    "入场",
    "上涨",
    "看涨",
    "看多",
    "涨",
    "盈利",
    "拉盘",
    "拉升",
    "主力进场",
    "买",
    "补",
    "追",
    "追涨",
    "流入",
    "发力",
    "吃肉",
    "多头",
    "赚",
    "涨幅",
    "大阳线",
    "阳线",
    "潜力无限",
    "业绩暴增",
    "业绩暴涨",
    "金叉",
    "大增",
    "提振",
]


def match_words(code):
    data = pd.read_csv(f"./output/data_{code}.csv", encoding="gbk", index_col=0)
    data = data.sort_values(by=["comment_date"])

    n = 0
    date_pre = data.iloc[0, 2]

    good_num_d = 0
    bad_num_d = 0

    rating = pd.DataFrame()
    words_day = pd.DataFrame()

    for i in range(len(data)):
        date = data.iloc[i, 2]
        if (date == date_pre) and (i != (len(data) - 1)):
            text = data.iloc[i, 0]
            words = jieba.lcut(text)
            good_matches = [word for word in words if word in good_words]
            bad_matches = [word for word in words if word in bad_words]

            comment_date = data.iloc[i, 1]
            comment_time = data.iloc[i, 2]
            t = pd.DataFrame(
                data=[
                    f"{good_matches}",
                    len(good_matches),
                    f"{bad_matches}",
                    len(bad_matches),
                    comment_date,
                    comment_time,
                ]
            )
            t = t.T
            t.columns = [
                "good_matches_day",
                "good_matches_num",
                "bad_matches_day",
                "bad_matches_num",
                "date",
                "time",
            ]
            words_day = pd.concat((words_day, t))

            good_num_d = good_num_d + len(good_matches)
            bad_num_d = bad_num_d + len(bad_matches)
            date_pre = date
        elif (date != date_pre) or (i == (len(data) - 1)):
            n = n + 1
            print(f"day{date_pre}  {i}")
            horizon = good_num_d - bad_num_d
            msum = good_num_d + bad_num_d
            if msum != 0:
                good_rate = good_num_d / msum
                bad_rate = bad_num_d / msum
            elif msum == 0:
                good_rate = 0
                bad_rate = 0

            tt = pd.DataFrame(
                data=[date_pre, good_num_d, bad_num_d, good_rate, bad_rate, horizon]
            ).T
            tt.columns = [
                "date",
                "good_matches_day",
                "bad_matches_day",
                "good_rate",
                "bad_rate",
                "horizon",
            ]
            rating = pd.concat((rating, tt))

            good_num_d = 0
            bad_num_d = 0
            text = data.iloc[i, 0]
            words = jieba.lcut(text)
            good_matches = [word for word in words if word in good_words]
            bad_matches = [word for word in words if word in bad_words]

            comment_date = data.iloc[i, 1]
            comment_time = data.iloc[i, 2]
            t = pd.DataFrame(
                data=[
                    f"{good_matches}",
                    len(good_matches),
                    f"{bad_matches}",
                    len(bad_matches),
                    comment_date,
                    comment_time,
                ]
            )
            t = t.T
            t.columns = [
                "good_matches_day",
                "good_matches_num",
                "bad_matches_day",
                "bad_matches_num",
                "date",
                "time",
            ]
            words_day = pd.concat((words_day, t))

            good_num_d = good_num_d + len(good_matches)
            bad_num_d = bad_num_d + len(bad_matches)
            date_pre = date

    rating = rating.reset_index(drop=True)
    rating.to_csv("./output/rating.csv", encoding="gbk", index_label=None)

    words_day = words_day.reset_index(drop=True)
    words_day.to_csv("./output/words_day.csv", encoding="gbk", index_label=None)

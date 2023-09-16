import time

import numpy as np
import pyecharts.options as opts
from pyecharts.charts import Line, Kline, Liquid, Grid, Pie, Calendar
import pandas as pd
import tushare as ts
import datetime

from pyecharts.commons.utils import JsCode


def fig_output_html():
    data = pd.read_csv("./output/rating.csv", encoding="gbk", index_col=0)

    # 一个月清晰变化曲线
    (
        Line(init_opts=opts.InitOpts(width="800px", height="400px"))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="8月份评论情绪", subtitle="词汇总"),
            tooltip_opts=opts.TooltipOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(type_="category"),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
        )
        .add_xaxis(xaxis_data=data.date)
        .add_yaxis(
            series_name="每日评论积极情绪词",
            y_axis=data.good_matches_day,
            symbol="emptyCircle",
            is_symbol_show=True,
            label_opts=opts.LabelOpts(is_show=False),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="最大值"),
                    opts.MarkPointItem(type_="min", name="最小值"),
                ]
            ),
            markline_opts=opts.MarkLineOpts(
                data=[opts.MarkLineItem(type_="average", name="平均值")]
            ),
        )
        .add_yaxis(
            series_name="每日评论消极情绪词",
            y_axis=data.bad_matches_day,
            markpoint_opts=opts.MarkPointOpts(
                data=[opts.MarkPointItem(value=-2, name="周最低", x=1, y=-1.5)]
            ),
            markline_opts=opts.MarkLineOpts(
                data=[
                    opts.MarkLineItem(type_="average", name="平均值"),
                    opts.MarkLineItem(symbol="none", x="90%", y="max"),
                    opts.MarkLineItem(symbol="circle", type_="max", name="最高点"),
                ]
            ),
        )
        .render("./templates/graphic/daily_comment_line.html")
    )

    # 一个月情绪变化水平线图
    (
        Line(init_opts=opts.InitOpts(width="800px", height="400px"))
        .add_xaxis(xaxis_data=data.date)
        .add_yaxis(
            series_name="",
            y_axis=data.horizon,
            # is_smooth=True,
            areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
            linestyle_opts=opts.LineStyleOpts(),
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="水平线"),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            datazoom_opts=[
                opts.DataZoomOpts(xaxis_index=0, range_start=0, range_end=100),
                opts.DataZoomOpts(
                    type_="inside", xaxis_index=0, range_start=0, range_end=100
                ),
            ],
            visualmap_opts=opts.VisualMapOpts(
                pos_top="10",
                pos_right="-10",
                is_piecewise=True,
                pieces=[
                    {"gt": -150, "lte": -100, "color": "#096"},
                    {"gt": -100, "lte": -50, "color": "#ffde33"},
                    {"gt": -50, "lte": 0, "color": "#ff9933"},
                    {"gt": 0, "lte": 50, "color": "#cc0033"},
                    {"gt": 50, "lte": 100, "color": "#660099"},
                    {"gt": 100, "color": "#7e0023"},
                ],
                out_of_range={"color": "#999"},
            ),
            xaxis_opts=opts.AxisOpts(type_="category"),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                name_location="start",
                min_=-200,
                max_=200,
                is_scale=True,
                axistick_opts=opts.AxisTickOpts(is_inside=False),
            ),
        )
        .set_series_opts(
            markline_opts=opts.MarkLineOpts(
                data=[
                    {"yAxis": -150},
                    {"yAxis": -100},
                    {"yAxis": -50},
                    {"yAxis": 50},
                    {"yAxis": 100},
                ],
                label_opts=opts.LabelOpts(position="end"),
            )
        )
        .render("./templates/graphic/daily_horizon.html")
    )

    word_comment = pd.read_csv("./output/words_day.csv", encoding="gbk", index_col=0)

    # 所有评论积极消极词汇统计
    (
        Line(init_opts=opts.InitOpts(width="800px", height="400px"))
        .add_xaxis(xaxis_data=word_comment.date)
        .add_yaxis(
            series_name="积极词数",
            y_axis=word_comment.good_matches_num,
            areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
            linestyle_opts=opts.LineStyleOpts(),
            label_opts=opts.LabelOpts(is_show=False),
            markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="min")]),
        )
        .add_yaxis(
            series_name="消极词数",
            y_axis=word_comment.bad_matches_num,
            yaxis_index=1,
            areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
            linestyle_opts=opts.LineStyleOpts(),
            label_opts=opts.LabelOpts(is_show=False),
            markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max")]),
        )
        .extend_axis(
            yaxis=opts.AxisOpts(
                name="消极词数",
                name_location="start",
                type_="value",
                max_=max(word_comment.good_matches_num),
                is_inverse=True,
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            )
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="评论统计",
                subtitle="所有评论",
                pos_left="center",
                pos_top="top",
            ),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            legend_opts=opts.LegendOpts(pos_left="left"),
            datazoom_opts=[
                opts.DataZoomOpts(range_start=90, range_end=100),
                opts.DataZoomOpts(type_="inside", range_start=90, range_end=100),
            ],
            xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
            yaxis_opts=opts.AxisOpts(
                name="积极词数", type_="value", max_=max(word_comment.bad_matches_num)
            ),
        )
        .set_series_opts(
            axisline_opts=opts.AxisLineOpts(),
        )
        .render("./templates/graphic/all_comment.html")
    )


def fig_kline(code, day):
    # k线图
    # day = '08-01'
    # code = 300059
    today = time.strftime("%Y-%m-%d", time.localtime())
    first_day = (datetime.datetime.strptime(day, "%m-%d")).strftime("2023-%m-%d")
    df = ts.get_k_data(f"{code}", start=first_day, end=today)
    df.set_index("date", inplace=True)
    df.head()

    df = pd.concat((df.iloc[:, 0:4].drop(columns=["high"]), df.high), axis=1)
    # df = df.reset_index()

    list_k = []
    for i in range(len(df)):
        list_k.append(list(df.iloc[i, :]))

    c = (
        Kline(init_opts=opts.InitOpts(width="800px", height="400px"))
        .add_xaxis(xaxis_data=list(df.index))
        .add_yaxis("kline", y_axis=list_k)
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(is_scale=True),
            yaxis_opts=opts.AxisOpts(
                is_scale=True,
                splitarea_opts=opts.SplitAreaOpts(
                    is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                ),
            ),
            datazoom_opts=(
                [
                    opts.DataZoomOpts(range_start=90, range_end=100),
                    opts.DataZoomOpts(type_="inside", range_start=90, range_end=100),
                ],
            ),
            title_opts=opts.TitleOpts(title=f"K 线图 - 代码：{code}"),
        )
        .render(f"./templates/graphic/kline_{code}.html")
    )


def liquid():
    data = pd.read_csv("./output/rating.csv", encoding="gbk", index_col=0)
    good_rate = data.iloc[-1, 3]
    bad_rate = data.iloc[-1, 4]
    l1 = (
        Liquid(init_opts=opts.InitOpts(width="800px", height="400px"))
        .add("lq", [bad_rate], center=["60%", "50%"], is_outline_show=False)
        .set_global_opts(title_opts=opts.TitleOpts(title=""))
    )

    l2 = Liquid(init_opts=opts.InitOpts(width="800px", height="400px")).add(
        "lq",
        [good_rate],
        center=["25%", "50%"], is_outline_show=False,
        label_opts=opts.LabelOpts(
            font_size=50,
            formatter=JsCode(
                """function (param) {
                        return (Math.floor(param.value * 10000) / 100) + '%';
                    }"""
            ),
            position="inside",
        ),

    )

    grid = Grid().add(l1, grid_opts=opts.GridOpts()).add(l2, grid_opts=opts.GridOpts())
    grid.render("./templates/graphic/main_liquid.html")


def fig_pie():
    data = pd.read_csv("./output/rating.csv", encoding="gbk", index_col=0)
    today = time.strftime("%m-%d", time.localtime())
    good_num = data.iloc[-1, 1]
    bad_num = data.iloc[-1, 2]
    (
        Pie(init_opts=opts.InitOpts(width="400px", height="400px"))
        .add(
            f"{today}评论词语统计",
            [list(z) for z in zip(['积极词语数', '消极词语数'], [int(good_num), int(bad_num)])],
            radius=["40%", "55%"],
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Pie-调整位置"),
            legend_opts=opts.LegendOpts(pos_left="15%"))
        .set_global_opts(title_opts=opts.TitleOpts(title=f"{today}评论词语统计", pos_top='50'))
        .render("./templates/graphic/pie_.html")
    )




def fig_calendar():
    data = pd.read_csv("./output/rating.csv", encoding="gbk", index_col=0)
    day = []
    for i in range(len(data)):
        day.append(datetime.datetime.strptime(data.iloc[i,0], "%m-%d").strftime("2023-%m-%d"))

    data_all = [list(z) for z in zip(day, data.horizon)]



    c = (
        Calendar(init_opts=opts.InitOpts(width="400px", height="400px"))
        .add("", data_all, calendar_opts=opts.CalendarOpts(range_=[day[0],day[-1]]))
        .set_global_opts(
            title_opts=opts.TitleOpts(title=f"{day[0]}~{day[-1]} 评论情绪热度情况"),
            visualmap_opts=opts.VisualMapOpts(
                max_=200,
                min_=-200,
                orient="vertical",
                is_piecewise=True,
                pos_top="230px",
                pos_left="100px",
            ),
        )
        .render("./templates/graphic/calendar.html")
    )
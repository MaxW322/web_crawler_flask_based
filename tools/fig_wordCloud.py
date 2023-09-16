import jieba
import pandas as pd
import pyecharts.options as opts
from pyecharts.charts import WordCloud

del_words = ['的', '了', '是', '今天', '就', '在', '我', '不', '都', '你', '还', '今年',
             '年', '有', '啊', '也', '明天', '和', '又', '要', '这', '吗', '】', '【',
             '（', '）', '(', ')', '!', '！', '.', '。', ',', '，', '?', '？', '\'', '\"', '’', '“', ';', ':', '：', '：']


def fig_wordcloud(code):
    df = pd.read_csv(f'./output/data_{code}.csv', index_col=0, encoding='gbk')
    all_day = pd.read_csv(f'./output/rating.csv', index_col=0, encoding='gbk')
    for date_time in all_day['date']:
        # 遍历每一天
        text = ''
        for j in range(len(df)):
            # 清洗数据
            if df.iloc[j, 2] == date_time:
                string = df.iloc[j, 0]
                for word in del_words:
                    n = string.count(word)
                    string = string.replace(word, '', n)
                text += string
        text = ' '.join(jieba.cut(text))
        data_dict = {}
        text = text.split(' ')
        for word in text:
            # 构造词云图的data数据结构
            if not (word in list(data_dict.keys())):
                data_dict[word] = 1
            else:
                data_dict[word] += 1
        data = []
        for key in data_dict.keys():
            data.append((key, data_dict[key]))

        # 生成词云图对象
        c = (
            WordCloud(init_opts=opts.InitOpts(width="400px", height="200px"))
            .add(series_name="热词", data_pair=data, word_size_range=[9, 66], shape='diamond',
                 textstyle_opts=opts.TextStyleOpts(font_family="cursive"))
            .set_global_opts(
                title_opts=opts.TitleOpts(title="热词", title_textstyle_opts=opts.TextStyleOpts(font_size=23)),
                tooltip_opts=opts.TooltipOpts(is_show=True), )
            .render(f"./templates/graphic/wordcloud/wordcloud_{date_time}.html")
        )
        print(f'生成词云 {date_time}')

# fig_wordcloud(300059) 测试使用

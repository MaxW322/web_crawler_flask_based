import time

from flask import Flask, render_template, request, session, url_for, jsonify, stream_with_context, Response, \
    make_response
from tqdm import tqdm

from fig_wordCloud import fig_wordcloud
from grab import grab_data
from load_data import DbProcess
from match import match_words
from fig_out import fig_output_html, fig_kline, liquid, fig_pie, fig_calendar
import datetime
import pandas as pd

app = Flask(__name__)

total = 5  # 总任务数
tasks = range(total)
pbar = tqdm(total=len(tasks))
db = DbProcess()
status = ''
code = 300059


@app.route('/')
def main():
    global code
    data = pd.read_csv(f"./output/data_{code}.csv", encoding="gbk", index_col=0)
    data = data.sort_values(by=["comment_date"])
    last_comment_text = data.iloc[-1, 0]
    last_comment_date = data.iloc[-1, 1]
    return render_template('main_page.html', last_comment_text=last_comment_text, last_comment_date=last_comment_date)


@app.route('/page_all')
def page2():
    data = pd.read_csv(f"./output/data_{code}.csv", encoding="gbk", index_col=0)
    data = data.sort_values(by=["comment_date"], ascending=False)
    data = data.iloc[0:100, 0:2]
    comments = data.to_dict('records')
    return render_template('page_all.html', comments=comments)


@app.route('/receive_code', methods=['POST'])
def handle_data():
    global status, code
    pbar.reset()
    data = request.json
    code = data['input_code']
    last_day = data['last_day']
    last_day_ = datetime.datetime.strptime(last_day, "%Y-%m-%dT%H:%M")
    day = last_day_.strftime("%m-%d")
    pbar.update(1)  # 20%
    status = '初始化'
    # 爬取数据
    status = '爬取数据'
    grab_data(code=code, day=day)
    pbar.update(1)  # 40%
    # 文本分析
    status = '文本分析'
    match_words(code)
    pbar.update(1)  # 60%
    # 作图
    status = '作图'
    fig_output_html()
    liquid()
    fig_kline(code, day)
    fig_wordcloud(code)
    fig_pie()
    fig_calendar()
    pbar.update(1)  # 80%
    # 导入数据库
    status = '导入数据库'
    db.load_csv(f"./output/data_{code}.csv")
    pbar.update(1)  # 100%
    status = '爬取完成'

    pbar.refresh()
    return '股票代码收到'


@app.route('/progress/')
def progress():
    """查看进度"""
    response = make_response(jsonify(dict(status=status, n=pbar.n, total=pbar.total)))
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', '*')
    return response


# 图
@app.route('/all_comment')
def all_comment():
    print(url_for('all_comment'))
    return render_template('./graphic/all_comment.html')


@app.route('/kline')
def kline():
    global code
    return render_template(f'./graphic/kline_{code}.html')


@app.route('/main_liquid')
def main_liquid():
    return render_template('./graphic/main_liquid.html')


@app.route('/main_wordcloud')
def main_wordcloud():
    today = time.strftime("%m-%d", time.localtime())
    return render_template(f'./graphic/wordcloud/wordcloud_{today}.html')


@app.route('/main_pie')
def main_pie():
    return render_template(f'./graphic/pie_.html')


@app.route('/daily_comment_line')
def daily_comment_line():
    return render_template(f'./graphic/daily_comment_line.html')


@app.route('/daily_horizon')
def daily_horizon():
    return render_template(f'./graphic/daily_horizon.html')


@app.route('/calendar')
def calendar():
    return render_template(f'./graphic/calendar.html')


if __name__ == '__main__':
    app.run(debug=True)

import logging
import random

import re

from tools.get_captcha import get_captcha_code_and_content
from tools.load_data import DbProcess

import time

from flask import Flask, render_template, request, session, url_for, jsonify, stream_with_context, Response, \
    make_response
from tqdm import tqdm

from tools.fig_wordCloud import fig_wordcloud
from tools.grab import grab_data
from tools.match import match_words
from tools.fig_out import fig_output_html, fig_kline, liquid, fig_pie, fig_calendar, get_last_day
import datetime
import pandas as pd

app = Flask(__name__)
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

app.secret_key = 'notes.zhengdonxu.com'
db = DbProcess()
db1 = db.get_db()
cur = db1.cursor()

total = 5  # 总任务数
current_statue = 0
tasks = range(total)
pbar = tqdm(total=len(tasks))
status = ''
code = 300059


@app.route('/')
def hello_world():
    is_login = session.get('is_login')
    return render_template('/index.html', is_login=is_login)


@app.route('/register')
def register_view():
    return render_template('register.html')


@app.route('/login')
def login_view():
    return render_template('login.html')


@app.post('/api/send_register_sms')
def send_register_sms():
    # 1.解析前端传递过来的数据
    data = request.get_json()
    mobile = data['mobile']

    # 2.校验手机号
    pattern = r'^1[3-9]\d{9}$'
    ret = re.match(pattern, mobile)
    if not ret:
        return {
            'message': '手机号不存在',
            'code': -1
        }
    # 3.发送短信验证码，并记录
    session['mobile'] = mobile
    # 3.1生产随机验证码
    code = random.choices('0123456789', k=6)
    session['code'] = ''.join(code)
    logging.warning(code)
    return {
        'message': '发送短信验证码成功',
        'code': 0
    }


@app.post('/api/register')
def register_api():
    # 1.解析传递过来的数据
    data = request.get_json()
    code1 = data['vercode']
    code2 = session['code']

    if code1 != code2:
        return {
            'message': '短信验证码错误',
            'code': '-1'
        }
    nickname = data['nickname']
    mobile = data['mobile']
    password = data['password']
    # 查找手机号是否注册
    cur.execute(f'select * from admin where mobile = {mobile}')
    result = cur.fetchone()
    print(result)
    if result is not None:
        return {
            'message': '手机号已注册',
            'code': '-1'
        }

    # 数据缺失
    if not all([nickname, mobile, password]):
        return {
            'message': '数据缺失',
            'code': -1
        }

    # 插入信息
    try:
        cur.execute(f'insert into admin values ("{nickname}",{mobile},"{password}")')
        db1.commit()
    except Exception as e:
        print(e)
        db1.rollback()

    return {
        'message': '注册用户成功',
        'code': 0
    }


@app.get('/get_captcha')
def get_captcha_view():
    # 1.获取参数
    captcha_uuid = request.args.get("captcha_uuid")
    # 2.生成验证码
    code, content = get_captcha_code_and_content()
    # 3.记录数据到数据库(用session代替)
    session['code'] = code
    resp = make_response(content)
    resp.content_type = "image/png"
    # 4. 返回响应体
    return resp


@app.post('/api/login')
def login_api():
    data = request.get_json()
    code = session['code']
    if code != data['captcha']:
        return {
            'message': '验证码错误',
            'code': -1
        }
    mobile = data["username"]
    cur.execute(f'select * from admin where mobile = "{mobile}"')
    ret = cur.fetchall()
    print(ret)
    if not ret:
        return {
            'message': '用户不存在',
            'code': -1
        }
    pwd = ret[0][2]
    if pwd != data['password']:
        return {
            'message': '密码错误',
            'code': -1
        }
    session['is_login'] = True  # 记录用户登陆成功
    return {
        'message': '用户登录成功',
        'code': 0
    }


@app.get('/api/quit')
def login_out_api():
    session['is_login'] = False
    return {
        'message': '退出登录成功',
        'code': 0
    }


@app.route('/api/search')
def all_information():
    page = request.args.get('page', type=int, default=1)
    per_page = request.args.get('limit', type=int, default=10)
    start = (page - 1) * per_page
    end = start + per_page
    comment_text = request.args.get('comment_text')
    if comment_text is None:
        cur.execute("select comment_text,comment_date from comment")
    else:
        cur.execute(f"select comment_text,comment_date from comment where comment_text like '%{comment_text}%'")
    rets = cur.fetchall()
    count = len(rets)
    rets = rets[start:end]
    return {
        'code': 0,
        'msg': '信息查询成功',
        'count': count,
        'data': [
            {
                'comment_text': ret[0],
                'create_at': ret[1]
            } for ret in rets
        ]
    }


# -------------------------------------------------------------------
@app.route('/main_page')
def main():
    global code
    data = pd.read_csv(f"./output/data_{code}.csv", encoding="gbk", index_col=0)
    data = data.sort_values(by=["comment_date"])
    last_comment_text = data.iloc[-1, 0]
    last_comment_date = data.iloc[-1, 1]
    return render_template('main_page.html', last_comment_text=last_comment_text,
                           last_comment_date=last_comment_date)


@app.route('/page_all')
def page2():
    data = pd.read_csv(f"./output/data_{code}.csv", encoding="gbk", index_col=0)
    data = data.sort_values(by=["comment_date"], ascending=False)
    data = data.iloc[0:100, 0:2]
    comments = data.to_dict('records')
    return render_template('page_all.html', comments=comments)


@app.route('/receive_code', methods=['POST'])
def handle_data():
    global status, code, current_statue
    pbar.reset()
    data = request.json
    code = data['input_code']
    last_day = data['last_day']
    last_day_ = datetime.datetime.strptime(last_day, "%Y-%m-%dT%H:%M")
    day = last_day_.strftime("%m-%d")
    pbar.update(1)  # 20%
    current_statue = 1
    status = '初始化'
    # 爬取数据
    status = '爬取数据'
    grab_data(code=code, day=day)
    pbar.update(1)  # 40%
    current_statue = 2
    # 文本分析
    status = '文本分析'
    match_words(code)
    pbar.update(1)  # 60%
    current_statue = 3
    # 作图
    status = '作图'
    fig_output_html()
    liquid()
    fig_kline(code, day)
    fig_wordcloud(code)
    fig_pie()
    fig_calendar()
    pbar.update(1)  # 80%
    current_statue = 4
    # 导入数据库
    status = '导入数据库'
    db.load_csv(f"./output/data_{code}.csv")
    pbar.update(1)  # 100%
    current_statue = 5
    status = '爬取完成'
    time.sleep(1)
    current_statue = 6

    pbar.refresh()
    return '股票代码收到'


@app.route('/progress/')
def progress():
    """查看进度"""
    response = make_response(jsonify(dict(status=status, n=current_statue, total=pbar.total)))
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
    # today = time.strftime("%m-%d", time.localtime())
    today = get_last_day()
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


@app.route('/page_search')
def page_search_view():
    return render_template('/page_search.html')


if __name__ == '__main__':
    # db.load_csv(f'./output/data_300059.scv')

    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = datetime.timedelta(seconds=1)
    app.run(debug=True)

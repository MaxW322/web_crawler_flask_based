## 股票评论爬取分析
### 实现 web 交互页面

![主页]https://github.com/MaxW322/web_crawler_flask_based/blob/5140e3e36c8f7873ebb13b418cf670b29a92dd0f/for_git_image/main_page.png)
![所有评论分析](https://github.com/MaxW322/web_crawler_flask_based/blob/5140e3e36c8f7873ebb13b418cf670b29a92dd0f/for_git_image/all_comment.png)
![评论搜索](https://github.com/MaxW322/web_crawler_flask_based/blob/5140e3e36c8f7873ebb13b418cf670b29a92dd0f/for_git_image/search_comment.png)

### 后端

- 选用 Flask 作为 web 框架
#### 爬取
- 基于 selenium 库
- webdriver 选择 Chrome
- 目标网页：https://guba.eastmoney.com/list,300059.html
- 爬取对象：评论文本，评论时间
- 实现
	- 使用`selenium.webdriver`用 Chrome 打开目标网页
	- 用`lxml.etree`遍历查找目标网页 html 
		- 找到`class="content"`，`class="basic_info"`
		- 将评论文本和评论时间存入 Dataframe 中
		- 导出 Dataframe 至 csv

#### 文本分析
- 读取爬取导出的 csv
- 打表：列表好词，坏词
- 使用 jieba 库将评论文本分词
	- 对分词后结果对应预先打好的列表，得到每日评论的好词坏词数量
	- 计算每日好词坏词比例，水平数据
	- 导出 csv

#### 图表绘制
- 基于 pyecharts 库
- 读取文本分析结果 csv
- 绘制
	- 按时间所有评论好坏词折现图
	- 每日好坏词比例
	- 每日好坏词水平线
	- 每日 重点词云图
		- jieba 库分词后，去除语气词等无用词汇，计数
		- pyecharts 绘制
	- 每日好坏词 pie 图
	- 基于 tushare 获取一段时间股票代码的情况
		- 绘制 k 线图
- 导出所有图为 html 格式

#### 数据导入数据库
- 基于 pymysql 库
	- 读取爬取结果的 csv
	- 逐行将爬取的文本，时间转化为数据库执行 sql 插入脚本

### 前端
#### 注册登陆界面
- 基于 captcha 库实现随机验证码

#### 评论搜索
- 搜索文本传值到后端，sql模糊搜索
#### 网页排版

- 图表插入
	- 所有图标都为 html 格式
	- 使用 iframe 标签嵌入到页面中
	- iframe 都在使用 css 设置好样式的 box 中，实现固定位置和背景
- 爬取信息输入和返回到后端
	- 使用 form 表单，input 标签来实现输入，默认300059
	- 时间选取使用 input 标签中 `datetime-local` 的 type 是实现
	- 按钮触发 js 脚本
		- .click 检测点击按钮之后，querySelector 获取表单中的 input 标签的值
		- 返回 json 到后端
		- 后端执行 爬取函数
	- 进度条实现
		- 在上同一个 js 脚本中，每秒使用 ajax 请求一次后端，得到当前进度值和总进度
		- 调整 `progress-bar` 的属性来实现进度变化
- 主页顶部最新爬取评论
	- 直接读取爬取数据的最新评论和对应评论时间
	- 直接使用 flask 中 render_templates 返回最新评论和对应评论时间
	- 评论样式 css 设置
- 所有评论页滚动评论
	- 直接读取爬取数据的最新100条评论和对应评论时间
	- 转化为字典，选择 record类型转化
	- 直接使用 flask 中 render_templates 返回字典
	- html 中使用`django`模板标签`{% for %}` 迭代字典中的各个元素（每个评论）
	- 评论样式同上
	- 最底层 box 只留下垂直滚动条
		- js 脚本计算每条评论的边界的偏移像素值
		- 计时器定时执行函数，滚动到下一条评论

#### 遇到问题
- 批量评论文本展示
	- 使用django中的模板标签`{% for %}`解决
- 网页爬取数据后刷新，js计时器出现问题
	- 更改进度条进度返回数据解决


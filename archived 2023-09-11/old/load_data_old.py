import pandas as pd
import pymysql as pm


class db_process:
    def __init__(self):
        self.db = pm.connect(
            host="localhost", user="root", password="admin", db="web_project", port=3306
        )
        print("连接数据库成功")
        self.cur = self.db.cursor()

    def load_csv(self, csv_file_path):
        data = pd.read_csv(csv_file_path, encoding="gbk", index_col=0)
        for i in range(len(data)):
            list = []
            list.append(str(i))
            for j in range(3):
                list.append(str(data.iloc[i, j]))
            self.cur.execute(
                f"INSERT INTO comment VALUES {list[0],list[1],list[2],list[3]}"
            )
            # self.cur.execute(f'INSERT INTO {table_name} VALUES ({i},{data.iloc[i,'comment_text']}, {data.iloc[i,'comment_date']}, {data.iloc[i,'comment_time']})')
            self.db.commit()


db = db_process()
db.load_csv("./output/300059.csv")

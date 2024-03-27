

import pymongo
import pymysql

# 保存至MongoDB数据库
class ZhilianPipeline(object):
    def process_item(self, item, spider):
        con = pymongo.MongoClient("mongodb://localhost:27017")
        con = pymongo.MongoClient(host='localhost', port=27017)

        # mysql 数据库连接
        db =pymysql.connect(host='127.0.0.1', user='root', password='123456', port=3306, database='flask_job',
                      charset='utf8')
        # 选择使用哪个数据库
        mydb = con['data']

        # 使用哪个集合
        myset = mydb['info']
        infomations = {'职位名称': item['poname'], '公司名称': item['coname'], '工作城市': item['city'], '薪资范围': item['providesalary'], '学历要求': item['degree'],
                         '公司类型': item['coattr'], '公司规模': item['cosize'], '工作经验': item['worktime'], '福利待遇': item['welfare']}

        # print(item)

        # 使用cursor()方法获取操作游标
        cursor = db.cursor()

        checkSQL = " select  count(*)  from  tb_job where number = '%s'" % item['number']

        # SQL 插入语句
        sql = "INSERT INTO tb_job(number, company_name, position_name, city,salary, degree,\
               company_logo, url,company_url, education, coattr, cosize, worktime, welfare, publish_time) \
                VALUES ('%s', '%s',  '%s',  '%s',  '%s','%s','%s', '%s',  '%s',  '%s',  '%s','%s', '%s',  '%s',  '%s') " %  \
              (item['number'],item['coname'],item['poname'],item['city'],item['providesalary'],item['degree'] \
               ,item['companyLogo'],item['url'],item['companyUrl'],item['education'],item['coattr'],item['cosize'] \
               ,item['worktime'],item['welfare'],item['publishTime'])

        try:
            cursor.execute(checkSQL)
            exist = cursor.fetchone()
            # print(exist[0])
            if exist[0] > 0:
                print(item['number'] +',' +item['poname'] + ' 已存在')
                db.close()
                return item
            cursor.execute(sql)  # 执行sql语句
            db.commit()
            print('插入:' + item['number'] +',' +item['poname'] + ' 成功')
        except Exception as e:
            db.rollback()  # 发生错误时回滚
            # print('错误..')
            print(e)
        # 关闭数据库连接
        db.close()

        # myset.insert(infomations)
        return item














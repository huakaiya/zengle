
import pymysql

def hoop(start, end):

    # mysql 数据库连接
    db = pymysql.connect(host='127.0.0.1', user='root', password='123456', port=3306, database='flask_job',
                         charset='utf8')

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    sql = " select  *  from  tb_job limit   %s, %s" % ( start, end )
    cursor.execute(sql)
    jobs = cursor.fetchall()
    for job in jobs:
        washdata(job, db)
    db.close()

def transformMoney(s):
    if s[-1] == '千':
        money0 = 1000
    elif s[-1] == '万':
        money0 = 10000
    else:
        money0 = 1
    return money0


def washdata(item, db):
    s = item[5].split('-')
    size = item[12].split('-')
    time = item[13].split('-')
    if len(s)>1:
        salary0 = float(s[0][:-1]) * transformMoney(s[0])
        if s[1][-1] == '天':  #特殊处理带天的薪酬
            salary1 = float(s[1][:-3]) * transformMoney(s[1])
        else:
            if s[1][-1] == '月':  # 特殊处理带天的薪酬
                salary1 = float(s[1][:-4]) * transformMoney(s[1])
            elif s[1][-1] == '时':  # 特殊处理带天的薪酬
                salary1 = float(s[1][:-3]) * transformMoney(s[1])
            elif s[1][-1] == '次':  # 特殊处理带天的薪酬
                salary1 = float(s[1][:-3]) * transformMoney(s[1])
            else:
                salary1 = float(s[1][:-1]) * transformMoney(s[1])

    else:
        salary0 = 0
        salary1 = 1
    if len(size)>1:
        cosize0 = float(size[0])
        cosize1 = float(size[1][:-1])
    else:
        cosize0 = 0
        cosize1 = 0
    if len(time)>1:
        worktime0 = float(time[0])
        worktime1 = float(time[1][:-1])
    else:
        worktime0 = 0
        worktime1 = 0

    cursor = db.cursor()
    sql = "INSERT INTO tb_job2(id, number, company_name, position_name, city,salary0,salary1, degree,\
                 company_logo, url,company_url, education, coattr, cosize0, cosize1, worktime0, worktime1, welfare, publish_time) \
                  VALUES (%d, '%s',  '%s', '%s','%s',%f, %f,  '%s',  '%s',  '%s','%s',  \
                  '%s',  '%s',  %f,  %f,  %f,  %f,  '%s',  '%s') " % \
          (item[0], item[1], item[2], item[3],item[4], salary0, salary1, item[6], item[7], item[8] \
           , item[9], item[10], item[11],  cosize0 ,cosize1 , worktime0, worktime1, item[14], item[15])
    try:
        # print(salary0, salary1)
        # print(worktime0, worktime1)
        # print(cosize0, cosize1)
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        db.rollback()  # 发生错误时回滚
        print(e)
    # print(item)

if __name__ == '__main__':
    start = 1
    total = 3404
    interval = 1000
    for i in range(start, total, interval):
        # print(i, interval)
        hoop(i, interval)
        print('处理完成:', i+interval)

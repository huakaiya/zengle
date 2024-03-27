
import time
import random
import pymysql
from selenium import webdriver

# 用selenium，爬取并存入数据库
class JobDescriptionSpider:
    def __init__(self):
        # 初始化 Selenium WebDriver
        self.driver = webdriver.Chrome()  # 你可以根据需要选择其他的浏览器驱动

    def crawl_job_descriptions(self):
        # 这里需要替换成你的实际数据库连接信息
        db = pymysql.connect(host='127.0.0.1', user='root', password='123456', port=3306, database='flask_job',
                             charset='utf8')
        cursor = db.cursor()
        sql = "SELECT id, url FROM tb_job2"
        cursor.execute(sql)
        jobs = cursor.fetchall()
        for job in jobs:
            job_id = job[0]
            job_url = job[1]

            # 使用 Selenium 打开网页并获取职位描述信息
            self.driver.get(job_url)
            time.sleep(random.uniform(1, 3))  # 等待页面加载完成

            try:
                description_element = self.driver.find_element_by_css_selector('.describtion__detail-content')
                description = description_element.text.strip() if description_element else None
            except Exception as e:
                print(f"Failed to extract description for job ID {job_id}: {str(e)}")
                continue

            # 更新数据库中的记录
            if description:
                update_sql = "UPDATE tb_job2 SET `desc` = %s WHERE id = %s"
                try:
                    cursor.execute(update_sql, (description, job_id))
                except Exception as e:
                    print(f"fail sql")
                    continue
                db.commit()

            # time.sleep(random.uniform(3, 5))  # 等待一段时间再进行下一次爬取


# 在脚本的其他部分调用爬虫
if __name__ == "__main__":
    spider = JobDescriptionSpider()
    spider.crawl_job_descriptions()

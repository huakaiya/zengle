
import time
import random
import pymysql
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy import Request
# 直接爬虫，没有用selenium
class JobDescriptionSpider(scrapy.Spider):
    name = 'job_description'
    allowed_domains = ['example.com']  # 修改为实际的域名

    def start_requests(self):
        # 这里需要替换成你的实际数据库连接信息
        db = pymysql.connect(host='127.0.0.1', user='root', password='123456', port=3306, database='flask_job',
                             charset='utf8')
        cursor = db.cursor()
        sql = "SELECT id, url FROM tb_job2 limit 1"
        cursor.execute(sql)
        jobs = cursor.fetchall()
        for job in jobs:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
                'Referer': 'https://www.example.com',  # 修改为实际的 Referer
            }
            yield Request(url=job[1], callback=self.parse, meta={'job_id': job[0]}, headers=headers)
            time.sleep(random.uniform(1, 3))  # 间隔1到3秒再发送请求，模拟人类操作
        db.close()

    def parse(self, response):
        job_id = response.meta['job_id']
        description = response.css('.describtion__detail-content::text').get()
        # 这里假设你的MySQL表中有一个名为'desc'的字段，用于保存职位描述信息
        # 需要根据实际情况修改字段名和更新逻辑
        if description:
            # 更新数据库中的记录
            db = pymysql.connect(host='127.0.0.1', user='root', password='123456', port=3306, database='flask_job',
                                 charset='utf8')
            cursor = db.cursor()
            update_sql = "UPDATE tb_job2 SET `desc` = %s WHERE id = %s"
            cursor.execute(update_sql, (description.strip(), job_id))
            db.commit()
            db.close()

            time.sleep(random.uniform(3, 5))  # 等待3到5秒再进行下一次爬取，模拟人类操作

# 在脚本的其他部分调用爬虫
if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(JobDescriptionSpider)
    process.start()

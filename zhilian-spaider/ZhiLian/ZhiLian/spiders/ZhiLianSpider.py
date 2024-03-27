
import json
import scrapy
import schedule
import time
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider
from ZhiLian.ZhiLian.items import ZhilianItem

class ZhilianspiderSpider(scrapy.Spider):
    name = 'ZhiLianSpider'
    allowed_domains = ['zhaopin.com']

    print("Java开发(9000300110000) UI设计师(17000500050000) Web前端(9000100030000) PHP(9000300150000)")
    print("Python(9000300160000) Android(9000600010000) 美工(17000500100000) 深度学习(9000200050000)")
    print("算法工程师(9000200070000) Hadoop(9000600010000) Node.js(17000500100000) C(9000300020000)")
    print("U3D(9000600050000) 硬件工程师(9000500460000) 单片机(9000500520000) ")
    type_id = input("-- 请输入工作类型序号: ")
    # 拼接初始化Url
    start_urls = [
        "https://fe-api.zhaopin.com/c/i/jobs/searched-jobs?pageNo=1&pageSize=20&jobType=" + type_id]



    cotype_list = ['国企: 1', '外商独资: 2', '代表处: 3', '合资: 4', '民营: 5', '股份制企业: 8', '上市公司: 9', '国家机关: 6', '事业单位: 10',
                   '银行: 11',
                   '医院: 12', '学校/下级学院: 13', '律师事务所: 14', '社会团体: 15', '港澳台公司: 16', '其它: 7']
    cosize_list = ['20人以下: 1', '20-99人: 2', '100-299人: 3', '300-499人: 8', '500-999人: 4', '1000-9999人: 5', '10000人以上: 6']
    custom_settings = {
        'LOG_LEVEL': 'INFO',
        'CONCURRENT_REQUESTS': 64
    }




    # 解析start_urls
    def parse(self, response):
        # 对应json数据中的data
        datas = json.loads(response.text)
        try:
            totalcount = int(datas['data']['page']['total'])
        except Exception:
            totalcount = 0

        if totalcount == 0:
            # 没有数据
            pass
        elif totalcount <= 270:
            if totalcount <= 90:
                yield scrapy.Request(
                    url=response.url,
                    dont_filter=True,
                    callback=self.parse_result
                )
            elif 90 < totalcount <= 180:
                for page in range(1, 3):
                    yield scrapy.Request(
                        url=str(response.url).replace('pageNo=1', f'pageNo={page}'),
                        dont_filter=True,
                        callback=self.parse_result
                    )
            else:
                for page in range(1, 4):
                    yield scrapy.Request(
                        url=str(response.url).replace('pageNo=1', f'pageNo={page}'),
                        dont_filter=True,
                        callback=self.parse_result
                    )
        else:
            for cotype in self.cotype_list:
                yield scrapy.Request(
                    url=str(response.url).replace('companyType=-1', f'companyType={cotype.split(": ")[1]}'),
                    dont_filter=True,
                    callback=self.parse_cotype
                )

    # 按公司类型解析
    def parse_cotype(self, response):
        datas = json.loads(response.text)
        try:
            totalcount = int(datas['data']['page']['total'])
        except Exception:
            totalcount = 0

        if totalcount == 0:
            pass
        elif totalcount <= 270:
            if totalcount <= 90:
                yield scrapy.Request(
                    url=response.url,
                    dont_filter=True,
                    callback=self.parse_result
                )
            elif 90 < totalcount <= 180:
                for page in range(1, 3):
                    yield scrapy.Request(
                        url=str(response.url).replace('pageNo=1', f'pageNo={page}'),
                        dont_filter=True,
                        callback=self.parse_result
                    )
            else:
                for page in range(1, 4):
                    yield scrapy.Request(
                        url=str(response.url).replace('pageNo=1', f'pageNo={page}'),
                        dont_filter=True,
                        callback=self.parse_result
                    )
        else:
            for cosize in self.cosize_list:
                yield scrapy.Request(
                    url=str(response.url).replace('companySize=-1', f'companySize={cosize.split(": ")[1]}'),
                    dont_filter=True,
                    callback=self.parse_cosize
                )

    # 按公司规模解析
    def parse_cosize(self, response):
        datas = json.loads(response.text)
        try:
            totalcount = int(datas['data']['page']['total'])
        except Exception:
            totalcount = 0

        if totalcount == 0:
            pass
        elif totalcount <= 270:
            if totalcount <= 90:
                yield scrapy.Request(
                    url=response.url,
                    dont_filter=True,
                    callback=self.parse_result
                )
            elif 90 < totalcount <= 180:
                for page in range(1, 3):
                    yield scrapy.Request(
                        url=str(response.url).replace('pageNo=1', f'pageNo={page}'),
                        dont_filter=True,
                        callback=self.parse_result
                    )
            else:
                for page in range(1, 4):
                    yield scrapy.Request(
                        url=str(response.url).replace('pageNo=1', f'pageNo={page}'),
                        dont_filter=True,
                        callback=self.parse_result
                    )
        else:
            for page in range(1, 4):
                yield scrapy.Request(
                    url=str(response.url).replace('pageNo=1', f'pageNo={page}'),
                    dont_filter=True,
                    callback=self.parse_result
                )

    # 对最终的结果进行解析
    def parse_result(self, response):
        item = ZhilianItem()
        datas = json.loads(response.text)
        try:
            data_list = datas['data']['list']
        except Exception:
            data_list = []

        if len(data_list) > 0:
            for data in data_list:
                item = {}

                item['number'] = data['number']
                item['companyLogo'] = data['companyLogo']
                item['publishTime'] = data['publishTime']
                item['education'] = data['education']
                item['url'] = data['positionUrl']
                item['companyUrl'] = data['companyUrl']

                # 职位名称
                item['poname'] = data['name']
                # 公司名称
                item['coname'] = data['company']
                # 工作城市
                item['city'] = data['workCity']
                # 薪资范围
                item['providesalary'] = data['salary']
                # 学历要求
                item['degree'] = data['education']
                # 公司类型
                item['coattr'] = data['property']
                # 公司规模
                item['cosize'] = data['companySize']
                # 工作经验
                item['worktime'] = data['workingExp']
                # 福利待遇
                item['welfare'] = data['name']
                # print(item)
                yield item









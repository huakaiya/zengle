# -*- codeing = utf-8 -*-
# Author: Redcomet
# QQ: 81040295 (有疑问，联系原作者)
# @Time :2022/3/9 10:00
# @Author: Administrator
# @File :jobApi.py
import operator
from sqlalchemy import or_
from flask import Blueprint, request
from sqlalchemy import func, distinct
from sqlalchemy.sql import label

from algorithm import ItemCF, UserCF
from base.code import ResponseCode, ResponseMessage
from base.core import db
from base.response import ResMsg
from models.model import chart_data
from models.job import getWords, Job, job_schema
from utils.mytool import formatDegree
from models.collect import Collect
from models.type import Type
from flask import request, jsonify

jobBp = Blueprint("job", __name__)

# 词云使用--分词接口
@jobBp.route('/getWordCut', methods=["GET"])
def getWordCut():
    res = ResMsg()
    result = getWords()
    res.update(code=ResponseCode.SUCCESS, data=result)
    return res.data
from flask import request

@jobBp.route('/collect-job', methods=["GET"])
def collect_job():
    res = ResMsg()
    jobid = request.args.get('jobid')
    userid = request.args.get('userid')

    # 检查是否已经收藏过了
    collect_record = Collect.query.filter_by(jobid=jobid, userid=userid).first()
    if collect_record:
        res.update(code=ResponseCode.ERROR, data="Job already collected by user")
        return res.data

    # 创建新的收藏记录
    new_collect = Collect(jobid=jobid, userid=userid)
    db.session.add(new_collect)
    db.session.commit()

    res.update(code=ResponseCode.SUCCESS, data="Job collected successfully")
    return res.data

@jobBp.route('/uncollect-job', methods=["GET"])
def uncollect_job():
    res = ResMsg()
    jobid = request.args.get('jobid')
    userid = request.args.get('userid')

    # 查找并删除对应的收藏记录
    collect_record = Collect.query.filter_by(jobid=jobid, userid=userid).first()
    if not collect_record:
        res.update(code=ResponseCode.ERROR, data="Job not found in collection")
        return res.data

    db.session.delete(collect_record)
    db.session.commit()

    res.update(code=ResponseCode.SUCCESS, data="Job uncollected successfully")
    return res.data
# Library搜索
# @jobBp.route('/get', methods=["GET"])
# def get():
#     res = ResMsg()
#     keyword = request.args.get('keyword')
#     userid = 1
#     # print(keyword)
#
#     result = db.session.query(Job).filter(
#         or_(
#             Job.position_name.like('%' + keyword + '%'),
#             Job.city.like('%' + keyword + '%'),
#             Job.degree.like('%' + keyword + '%')
#         )
#     ).order_by(Job.publish_time.desc()).limit(8).all()
#
#     data = job_schema.dump(result)
#     res.update(code=ResponseCode.SUCCESS, data=data)
#     return res.data
@jobBp.route('/get', methods=["GET"])
def get():
    res = ResMsg()
    keyword = request.args.get('keyword')
    userid = 1  # 这里假设用户id为1
    # print(keyword)

    result = db.session.query(Job).filter(
        or_(
            Job.position_name.like('%' + keyword + '%'),
            Job.city.like('%' + keyword + '%'),
            Job.degree.like('%' + keyword + '%')
        )
    ).order_by(Job.publish_time.desc()).limit(8).all()

    # 遍历查询数据，设置flag字段
    for job in result:
        collect_record = Collect.query.filter_by(jobid=job.id, userid=userid).first()
        if collect_record:
            job.flag = True
        else:
            job.flag = False

    data = job_schema.dump(result)
    res.update(code=ResponseCode.SUCCESS, data=data)
    return res.data

@jobBp.route('/getper', methods=["GET"])
def getper():
    res = ResMsg()
    keyword = request.args.get('keyword')
    userid = 1  # 假设用户id为1

    # 查询用户收藏的职位id列表
    collected_job_ids = [collect.jobid for collect in Collect.query.filter_by(userid=userid).all()]

    # 查询包含关键字的职位，并且是用户已收藏的职位
    result = db.session.query(Job).filter(
        or_(
            Job.position_name.like('%' + keyword + '%'),
            Job.city.like('%' + keyword + '%'),
            Job.degree.like('%' + keyword + '%')
        ),
        Job.id.in_(collected_job_ids)  # 过滤已收藏的职位
    ).order_by(Job.publish_time.desc()).limit(8).all()
    # 遍历查询数据，设置flag字段
    for job in result:
        collect_record = Collect.query.filter_by(jobid=job.id, userid=userid).first()
        if collect_record:
            job.flag = True
        else:
            job.flag = False
    data = job_schema.dump(result)
    res.update(code=ResponseCode.SUCCESS, data=data)
    return res.data



# 热门 / 最新
@jobBp.route('/getHot', methods=["GET"])
def getHot():
    res = ResMsg()
    # result = db.session.query(Job).order_by(Job.publish_time.desc()).all()[:4]
    result = db.session.query(Job).order_by(Job.publish_time.desc()).limit(4).all()
    data = job_schema.dump(result)
    res.update(code=ResponseCode.SUCCESS, data=data)
    return res.data

# 推荐 --停用
@jobBp.route('/getRec', methods=["GET"])
def getRec():
    res = ResMsg()
    # result = db.session.query(Job).filter(Job.type.like('%科幻%')).order_by(Job.rate.desc()).all()[:4]
    # data = job_schema.dump(result)
    # res.update(code=ResponseCode.SUCCESS, data=data)
    return res.data


@jobBp.route('/getChart1', methods=["GET"])
def getChart1():
    res = ResMsg()
    all = []
    dz = []
    kh = []
    aq = []
    xj = []
    ranges = [('1900', '1950'), ('1950', '1960'), ('1960', '1970'), ('1970', '1980'), ('1980', '1990'),
              ('1990', '2000'), ('2000', '2010'), ('2010', '2020'), ('2020', '2030')]
    for r in ranges:
        cnt = db.session.query(Job).filter(Job.myear >= r[0], Job.myear < r[1]).count()
        dzcnt = db.session.query(Job).filter(Job.type.like('%动作%'), Job.myear >= r[0], Job.myear < r[1]).count()
        khcnt = db.session.query(Job).filter(Job.type.like('%科幻%'), Job.myear >= r[0], Job.myear < r[1]).count()
        aqcnt = db.session.query(Job).filter(Job.type.like('%爱情%'), Job.myear >= r[0], Job.myear < r[1]).count()
        xjcnt = db.session.query(Job).filter(Job.type.like('%喜剧%'), Job.myear >= r[0], Job.myear < r[1]).count()

        chart = dict(name=r[0] + '-' + r[1], value=cnt)
        all.append(chart)
        chart2 = dict(name=r[0] + '-' + r[1], value=dzcnt)
        dz.append(chart2)
        chart3 = dict(name=r[0] + '-' + r[1], value=khcnt)
        kh.append(chart3)
        chart4 = dict(name=r[0] + '-' + r[1], value=aqcnt)
        aq.append(chart4)
        chart5 = dict(name=r[0] + '-' + r[1], value=xjcnt)
        xj.append(chart5)
    # data = chart_data.dump(result)
    res.update(code=ResponseCode.SUCCESS, data=dict(all=all, kh=kh, dz=dz, aq=aq, xj=xj))
    return res.data


@jobBp.route('/getAreaChart', methods=["GET"])
def getAreaChart():
    res = ResMsg()
    kh = []
    ranges = [('1900', '1970'), ('1970', '1990'), ('1990', '2000'), ('2000', '2010'), ('2010', '2020')]
    for r in ranges:
        khcnt = db.session.query(Job).filter(Job.myear >= r[0], Job.myear < r[1]).count()
        chart3 = dict(name=r[0] + '-' + r[1], value=khcnt)
        kh.append(chart3)
    # data = chart_data.dump(result)
    res.update(code=ResponseCode.SUCCESS, data=dict(kh=kh))
    return res.data

@jobBp.route('/getChart2', methods=["GET"])
def getChart2():
    res = ResMsg()
    datas = []
    for i in range(2001, 2021):
        cnt = db.session.query(Job).filter(Job.myear == i).count()
        chart = dict(name=i, value=cnt)
        datas.append(chart)
    res.update(code=ResponseCode.SUCCESS, data=datas)
    return res.data

@jobBp.route('/getChart3', methods=["GET"])
def getChart3():
    res = ResMsg()
    result = db.session.query(Job.myear.label('name'), func.count('*').label('value')).group_by(Job.myear).order_by(
        Job.myear.asc()).all()
    datas = chart_data.dump(result)
    res.update(code=ResponseCode.SUCCESS, data=datas)
    return res.data

@jobBp.route('/getNationRank', methods=["GET"])
def getNationRank():
    res = ResMsg()
    nations = ['摩纳哥', '西班牙', '印度', '比利时', '塞浦路斯', '英国', '冒险', '韩国', '希腊', '奥地利', '意大利', '动画', '德国', '泰国', '喜剧', '澳大利亚',
               '中国台湾', '巴西', '中国香港', '墨西哥', '加拿大', '匈牙利', '中国大陆', '瑞典', '新西兰', '卡塔尔', '捷克', '瑞士', '南非', '法国', '伊朗',
               '黎巴嫩', '阿联酋', '日本', '悬疑', '约旦', '爱尔兰', '波兰', '丹麦', '美国', '阿根廷', '荷兰']
    datas = []
    for t in nations:
        cnt = db.session.query(Job).filter(Job.nation.like('%' + t + '%')).count()
        chart = dict(name=t, value=cnt)
        datas.append(chart)
    datas = sorted(datas, key=operator.itemgetter('value'), reverse=True)

    res.update(code=ResponseCode.SUCCESS, data=dict(datas=datas))
    return res.data


# @JobBp.before_request
# def init_session():
#     db.session = db.session.session_factory()

# 不同城市，不同学历的收入情况
@jobBp.route('/getTypeRate', methods=["GET"])
def getTypeRate():
    res = ResMsg()
    types = ['上海','北京','深圳','广州','苏州']

    datas = []
    for t in types:
        data = []
        jobs = db.session.query(Job).filter(Job.city.like('%' + t + '%'), Job.salary1!=0).all()
        for m in jobs:
            rateData = []
            rateData.append(formatDegree(m.degree))
            rateData.append(m.salary1)
            rateData.append(m.degree)
            rateData.append(m.salary0)
            rateData.append(m.position_name)
            rateData.append(m.company_name)
            data.append(rateData)
        datas.append(data)
    res.update(code=ResponseCode.SUCCESS, data=dict(datas=datas, labels=types))
    return res.data

@jobBp.route('/getTimeLine', methods=["GET"])
def getTimeLine():
    res = ResMsg()
    types = ['美国', '英国', '日本', '中国香港', '中国大陆', '法国', '德国', '韩国', '意大利', '加拿大','中国台湾','澳大利亚','西班牙','印度','瑞士','新西兰']
    datas = []
    for y in range(2000, 2021):
        yearData = []
        for t in types:
            cnt = db.session.query(Job).filter(Job.myear==y, Job.nation.like('%' + t + '%')).count()
            yearData.append(cnt)
        datas.append(yearData)

    res.update(code=ResponseCode.SUCCESS, data=dict(datas=datas))
    return res.data

# Flask 推荐算法接口（基于itemCF）
# 只推荐A领域的东西给目标用户，因为目标用户的主要兴趣点在A领域，
# 这样他有限的推荐列表中就会包含该领域一定数量不热门的物品，所以推荐长尾能力较强，但多样性不足
# 举例： 电影、购物、音乐网站等
@jobBp.route('/getRecomendation', methods=["GET"])
def getRecomendation():
    userId = request.args.get('userId')
    userId = int(userId)
    res = ResMsg()
    rates = []
    dd = []
    datas = ItemCF.recommend(userId)
    for id, rate in datas:
        print(id)
        item = db.session.query(Job).filter(Job.id == id).first()
        dd.append(item)
        rates.append(rate)
    data = job_schema.dump(dd)
    res.update(code=ResponseCode.SUCCESS, data=dict(datas=data, rates=rates))
    return res.data

# Flask 推荐算法接口（基于userCF）
# 系统会找到与目标用户兴趣相似的其他用户然后将其他用户关注的东西推荐给目标用户，所以是某个群体内的热门物品；
# 同时也反应出如果某些物品没有被该群体关注，则不会推荐给该群体，即推荐长尾能力的不足
# 举例： 微博热搜、热点新闻等
@jobBp.route('/getRecomendation2', methods=["GET"])
def getRecomendation2():
    userId = request.args.get('userId')
    userId = int(userId)
    res = ResMsg()
    datas = UserCF.recommend(userId)
    dd = []
    rates = []
    for id, rate in datas:
        # print(id)
        item = db.session.query(Job).filter(Job.id==id).first()
        dd.append(item)
        rates.append(rate)
    data = job_schema.dump(dd)
    res.update(code=ResponseCode.SUCCESS, data=dict(datas=data, rates=rates))
    return res.data

# 获取几个统计数字
@jobBp.route('/getPanel', methods=["GET"])
def getPanel():
    res = ResMsg()
    cnt1 = db.session.query(Job).count()
    cnt2 = db.session.query(func.count(distinct(Job.city))).scalar()
    cnt3 = db.session.query(func.count(distinct(Job.company_name))).scalar()
    cnt4 = db.session.query(func.count(distinct(Job.coattr))).scalar()

    res.update(code=ResponseCode.SUCCESS, data=dict(data1=cnt1, data2=cnt2, data3=cnt3, data4=cnt4))
    return res.data

# 职位按照份来分组统计
@jobBp.route('/getCityJob', methods=["GET"])
def getCityJob():
    res = {"code": 0, "data": [], "msg": "Success"}
    try:
        result = db.session.query(func.cast(Job.city, db.String).label('city'),
                                  func.count('*').label('value')).group_by(
            func.cast(Job.city, db.String)).order_by(Job.city.asc()).all()

        # 将城市转换为省份
        modified_result = []
        for row in result:
            city = row.city
            if city in city_to_province:
                province_name = city_to_province[city]
            else:
                province_name = city

            # 检查省份是否已经在 modified_result 中
            existing_province = next((item for item in modified_result if item['name'] == province_name), None)
            if existing_province:
                existing_province['value'] += row.value
            else:
                modified_result.append({'name': province_name, 'value': row.value})

        res['data'] = modified_result
    except Exception as e:
        res['code'] = -1
        res['msg'] = str(e)

    return jsonify(res)
city_to_province = {
    "上海": "上海市",
    "三亚": "海南",
    "三明": "福建",
    "上饶": "江西",
    "东莞": "广东",
    "中山": "广东",
    "临沂": "山东",
    "丹东": "辽宁",
    "丽水": "浙江",
    "乌鲁木齐": "新疆维吾尔自治区",
    "九江": "江西",
    "佛山": "广东",
    "保定": "河北",
    "六安": "安徽",
    "其他": "其他",
    "凉山": "四川",
    "包头": "内蒙古自治区",
    "北京": "北京市",
    "南京": "江苏",
    "南充": "四川",
    "南宁": "广西壮族自治区",
    "南昌": "江西",
    "南通": "江苏",
    "南阳": "河南",
    "厦门": "福建",
    "合肥": "安徽",
    "吉林市": "吉林",
    "呼伦贝尔": "内蒙古自治区",
    "呼和浩特": "内蒙古自治区",
    "咸阳": "陕西",
    "哈尔滨": "黑龙江",
    "唐山": "河北",
    "嘉兴": "浙江",
    "四川": "四川",
    "大庆": "黑龙江",
    "大连": "辽宁",
    "天水": "甘肃",
    "天津": "天津市",
    "太原": "山西",
    "威海": "山东",
    "宁德": "福建",
    "宁波": "浙江",
    "安阳": "河南",
    "宜昌": "湖北",
    "宝鸡": "陕西",
    "宣城": "安徽",
    "宿迁": "江苏",
    "岳阳": "湖南",
    "常州": "江苏",
    "常德": "湖南",
    "广州": "广东",
    "廊坊": "河北",
    "开封": "河南",
    "张家口": "河北",
    "徐州": "江苏",
    "德州": "山东",
    "惠州": "广东",
    "成都": "四川",
    "扬州": "江苏",
    "承德": "河北",
    "新乡": "河南",
    "无锡": "江苏",
    "日本": "日本",
    "日照": "山东",
    "昆明": "云南",
    "晋中": "山西",
    "晋城": "山西",
    "景德镇": "江西",
    "本溪": "辽宁",
    "杭州": "浙江",
    "枣庄": "山东",
    "株洲": "湖南",
    "桂林": "广西壮族自治区",
    "梧州": "广西壮族自治区",
    "榆林": "陕西",
    "武汉": "湖北",
    "毕节": "贵州",
    "江门": "广东",
    "沈阳": "辽宁",
    "沧州": "河北",
    "泉州": "福建",
    "泰安": "山东",
    "泰州": "江苏",
    "洛阳": "河南",
    "济南": "山东",
    "济宁": "山东",
    "海口": "海南",
    "海西": "青海",
    "淄博": "山东",
    "淮安": "江苏",
    "深圳": "广东",
    "清远": "广东",
    "温州": "浙江",
    "湖州": "浙江",
    "湘潭": "湖南",
    "湛江": "广东",
    "滨州": "山东",
    "漳州": "福建",
    "潍坊": "山东",
    "濮阳": "河南",
    "烟台": "山东",
    "焦作": "河南",
    "玉林": "广西壮族自治区",
    "珠海": "广东",
    "琼海": "海南",
    "眉山": "四川",
    "石家庄": "河北",
    "福州": "福建",
    "秦皇岛": "河北",
    "绍兴": "浙江",
    "绵阳": "四川",
    "美国": "美国",
    "舟山": "浙江",
    "芜湖": "安徽",
    "苏州": "江苏",
    "莆田": "福建",
    "菏泽": "山东",
    "蚌埠": "安徽",
    "衡水": "河北",
    "衡阳": "湖南",
    "襄阳": "湖北",
    "西咸新区": "陕西",
    "西宁": "青海",
    "西安": "陕西",
    "许昌": "河南",
    "贵阳": "贵州",
    "赤峰": "内蒙古自治区",
    "连云港": "江苏",
    "通辽": "内蒙古自治区",
    "邯郸": "河北",
    "郑州": "河南",
    "郴州": "湖南",
    "鄂尔多斯": "内蒙古自治区",
    "重庆": "重庆市",
    "金华": "浙江",
    "铜陵": "安徽",
    "银川": "宁夏回族自治区",
    "镇江": "江苏",
    "长春": "吉林",
    "长沙": "湖南",
    "长治": "山西",
    "阜阳": "安徽",
    "雅安": "四川",
    "青岛": "山东",
    "鞍山": "辽宁",
    "韶关": "广东",
    "香港": "香港特别行政区",
    "马鞍山": "安徽",
    "鹤壁": "河南",
    "鹰潭": "江西",
    "齐齐哈尔": "黑龙江"
}
@jobBp.route('/getProvinceJob', methods=["GET"])
def getProvinceJob2():
    res = {"code": 0, "data": [], "msg": "Success"}
    try:
        result = db.session.query(func.cast(Job.city, db.String).label('city'), func.count('*').label('value')).group_by(
            func.cast(Job.city, db.String)).order_by(Job.city.asc()).all()

        # 将城市转换为省份
        modified_result = []
        for row in result:
            city = row.city
            if city in city_to_province:
                province_name = city_to_province[city]
            else:
                province_name = city

            # 检查省份是否已经在 modified_result 中
            existing_province = next((item for item in modified_result if item['name'] == province_name), None)
            if existing_province:
                existing_province['value'] += row.value
            else:
                modified_result.append({'name': province_name, 'value': row.value})

        res['data'] = modified_result
    except Exception as e:
        res['code'] = -1
        res['msg'] = str(e)

    return jsonify(res)


# 职位按照城市来分组统计
@jobBp.route('/getCityJob2', methods=["GET"])
def getCityJob2():
    res = ResMsg()
    result = db.session.query(Job.city.label('name'), func.count('*').label('value')).group_by(Job.city).order_by(
        Job.city.asc()).all()
    datas = chart_data.dump(result)
    res.update(code=ResponseCode.SUCCESS, data=datas)
    return res.data

# 按照公司类型分组统计
@jobBp.route('/getTypeRank', methods=["GET"])
def getTypeRank():
    res = ResMsg()
    result = db.session.query(Job.coattr.label('name'), func.count('*').label('value')).group_by(Job.coattr).order_by(
        func.count('*').desc()).all()
    datas = chart_data.dump(result)
    res.update(code=ResponseCode.SUCCESS, data=datas)
    return res.data

# 按照需求的学历分组统计
@jobBp.route('/getDegreeRank', methods=["GET"])
def getDegreeRank():
    res = ResMsg()
    result = db.session.query(Job.degree.label('name'), func.count('*').label('value')).group_by(Job.degree).order_by(
        func.count('*').desc()).all()
    datas = chart_data.dump(result)
    res.update(code=ResponseCode.SUCCESS, data=datas)
    return res.data

@jobBp.after_request
def close_session(response):
    db.session.close()
    return response

# 后台方法，获取所有分类名称
@jobBp.route('/get_all_types', methods=["GET"])
def get_all_types():
    # 查询 type 表中的所有分类名称
    types = Type.query.with_entities(Type.name).all()
    # 将分类名称从元组列表中提取出来
    type_names = [type[0] for type in types]
    return jsonify({'types': type_names})

# 后台方法，根据分类名称获取 type 表数据
@jobBp.route('/dash3', methods=["GET"])
def get_type_data():
    # 获取请求参数中的分类名称
    type_name = request.args.get('type')

    # 查询 type 表中特定分类名称的数据
    type_data = Type.query.filter_by(name=type_name).first()

    # 如果没有找到数据，返回空数组
    if not type_data:
        return jsonify({'titles': [], 'contents': []})
    # 去掉排除ascii编码（英文编码）的字符串。  if not item.strip().isascii()
    desc_array = [item for item in type_data.descstr.split(',')]

    # 返回数据给前端
    return jsonify({'titles': desc_array, 'contents': desc_array})

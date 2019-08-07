import json
import time

import lxml
import requests
from bs4 import BeautifulSoup
from lxml import etree

positions = []

header = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-XA;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Cookie': 'JSESSIONID=ABAAABAAADEAAFI6A024DA411D131B8047C593743DCE5E4; WEBTJ-ID=20190802092635-16c4fef902f591-000c8d93e973ae-3f71045b-1049088-16c4fef903084b; _ga=GA1.2.1365396146.1564709196; _gid=GA1.2.2003995460.1564709196; user_trace_token=20190802092636-91b8c217-b4c4-11e9-86ab-525400f775ce; LGSID=20190802092636-91b8c34d-b4c4-11e9-86ab-525400f775ce; PRE_UTM=; PRE_HOST=cn.bing.com; PRE_SITE=https%3A%2F%2Fcn.bing.com%2F; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fgongsi%2F2-0-0-0; LGUID=20190802092636-91b8c565-b4c4-11e9-86ab-525400f775ce; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216c4ff0595151-0dcb53582bee94-3f71045b-1049088-16c4ff0595264b%22%2C%22%24device_id%22%3A%2216c4ff0595151-0dcb53582bee94-3f71045b-1049088-16c4ff0595264b%22%7D; sajssdk_2015_cross_new_user=1; _gat=1; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1564709313,1564709314; LG_HAS_LOGIN=1; _putrc=0CF1F6A70801DB5B123F89F2B170EADC; login=true; hasDeliver=0; gate_login_token=c9667036f0ddd18a93303dc5520c93ed3b1b70544ab59818306687b6e101f578; unick=%E5%BC%A0%E7%8E%89%E7%8E%BA; index_location_city=%E5%8C%97%E4%BA%AC; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1564709509; privacyPolicyPopup=false; TG-TRACK-CODE=index_navigation; X_HTTP_TOKEN=67d9a47186c09eaf9159074651b4e16dd387d6c087; LGRID=20190802093159-528d3715-b4c5-11e9-86ab-525400f775ce; SEARCH_ID=051ce5346cc14910ba99dcf44d70fdd9',
    'DNT': '1',
    'Host': 'www.lagou.com',
    'Referer': 'https://www.lagou.com/zhaopin/Python/?labelWords=label',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'X-Anit-Forge-Code': '0',
    'X-Anit-Forge-Token': None,
    'X-Requested-With': 'XMLHttpRequest'
}


# header = {'Host': 'www.lagou.com',
#           'Referer': 'https://www.lagou.com/jobs/list_Java?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords=&suginput=',
#           'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Mobile Safari/537.36',
#           'X-Anit-Forge-Code': '0',
#           'X-Anit-Forge-Token': None,
#           'X-Requested-With': 'XMLHttpRequest'}
for x in range(1, 31):
    if(x == 1):
        y = 'true'
    else:
        y = 'false'
    data = {'first': y, 'pn': x, 'kd': 'Python'}
    urls = "https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false"
    # r = requests.post(url=urls, headers=header, data=data)
    r = requests.get(url=urls, headers=header, data=data)
    json_result = r.json()  # 将爬取得网页转化成json格式
    print(json_result)
    # 获取每页我们需要的内容
    position_page = json_result['content']['positionResult']['result']
    for position in position_page:
        position_dict = {"岗位名称": position['positionName'],
                         '地点': position['city'],
                         '公司名称': position['companyFullName'],
                         '薪水': position['salary'],
                         '工作经验': position['workYear'],
                         }  # 通过字典存储的我们的信息
        positions.append(position_dict)
    line = json.dumps(positions, ensure_ascii=False)  # 将字典转化为json
    time.sleep(20)  # 因为拉钩的反扒机制，频率太快就会被限制，所以睡眠一下
    with open('lagou.json', 'w') as fp:
        fp.write(line)
        print("第%d已经爬取完毕" % x)
print('爬取完成')

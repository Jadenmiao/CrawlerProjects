import requests
from bs4 import BeautifulSoup
import re
import os

ul = 'https://www.bjsubway.com/station/zjgls/#'
response = requests.get(ul)
response.encoding = 'gbk'  # 原始网页编码错误，utf-8也不管用，只能用gbk
html = response.text
# print(html)
soup = BeautifulSoup(html, 'lxml')  # 变成汤汁


def get_txt_name():  # 得到线路名称的前一步
    txt_src_name = []
    for i in range(5, 10):
        temp = soup.find_all('td', {'colspan': str(i)})
        txt_src_name += temp
    return txt_src_name
    # 格式如[<td colspan="6">15号线相邻站间距信息统计表</td>, <td colspan="6">昌平线相邻站间距信息统计表</td>]
# print(get_txt_name())  # 测试用


def get_txtuseful_name():  # 得到可用的线路名称
    obj = []
    for each in get_txt_name():
        temp = re.findall(r">(.+?)<", str(each))  # 从>匹配到<(不包含)，若要包含，则先使用re.compile，再search
        obj += temp
    return obj
# print(get_txtuseful_name())  # 测试用


Stationinfo = soup.find_all('tbody')


def get_stationinfo():
    obj = []
    for each in Stationinfo:
        temp = re.findall(r">(.+?)<", str(each))
        obj += temp
    return obj
# print(get_stationinfo())


station_list = get_stationinfo()
# print(station_list)
os.makedirs('./线路图/', exist_ok=True)
with open('./线路图/test.txt', 'w') as f:  # 不能是wb，编码有问题，或者str转换成byte
    for line in station_list:
        if line == '上行/下行':
            f.write(line + '\n')
        else:
            f.write(line + ' ' * 10)  # 多来几个空格显得好看一点

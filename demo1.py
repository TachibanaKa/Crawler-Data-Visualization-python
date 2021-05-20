import re
import requests
import random
import time
from bs4 import BeautifulSoup
from pyecharts.charts import Bar,Line,Page,Pie
from pyecharts import options as opts

#  避免被拉黑
user_agent_list = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]
UA = random.choice(user_agent_list)  
headers = {'User-Agent': UA}  

#  目标网址
url = 'https://wh.zu.ke.com/zufang/pg'

#  要获取的信息
title_list = []     #  标题
price_list = []     #  租金
position_list = []  #  地理位置
size_list = []      #  房子面积

#  开始循环爬取每一页的信息
for x in range(2, 41):
    time.sleep(random.randint(2, 5))  #  避免被拉黑
    with requests.get(url+str(x), headers=headers, timeout=5) as response:
        soup = BeautifulSoup(response.content, 'lxml')
        print('======'  + '正在爬取第{}个网页'.format(x) + '======')
        #  获取包裹信息的div大盒子
        li_list = soup.find('div', class_='content__list').find_all('div')
        #  循环div大盒子里的每一条房子信息
        for li_quick in li_list:
            try:
                # 取房子名字
                title = li_quick.find('a', class_='twoline').get_text().strip()
                # 取租金
                price = li_quick.find('span', class_='content__list--item-price').find('em').get_text().strip()
                # 取位置信息
                position = li_quick.find('p', class_='content__list--item--des').find('a').get_text().strip()
                # 取面积
                temp_size = li_quick.find('p',class_='content__list--item--des').get_text().strip()
                size = re.findall(r'\d+㎡',temp_size)
            except:
                continue
            finally:
                if li_list.index(li_quick) % 2 == 0:
                    title_list.append(title)
                    price_list.append(price)
                    position_list.append(position)
                    size_list.append(''.join(size).strip('㎡'))

#  各区域房源数量
area_num_dict = {}
for i in position_list:
    area_num_dict[i] = area_num_dict.get(i, 0)+1

#  各区域房源的平均价
average_price_dict = {}
sum = 0
    #  把各地区房源价格集合在一起
for i in range(len(position_list)):
    if position_list[i] in average_price_dict:
        average_price_dict[position_list[i]]+=[price_list[i]]
    else:
        average_price_dict[position_list[i]]=[price_list[i]]
    #  求平均值
for i in average_price_dict:
    n = len(average_price_dict[i])
    for j in average_price_dict[i]:
        sum = sum+float(j)
    average_price_dict[i] = round(sum/n,0)
    sum = 0

#  各区域房源户型数量
area_room_type = []
area_room_type_dict = {}
    #  取出标题中的户型信息
for i in title_list:
    temp = re.findall(r'\s+\d',i)
    area_room_type.append(''.join(temp).strip()+'居室')
    #  整合户型数量
for i in area_room_type:
    area_room_type_dict[i] = area_room_type_dict.get(i, 0)+1

#  各区域房源面积区间占比
area_room_size_dict = {'1-20㎡':0,'20-40㎡':0,'40㎡以上':0,}
for i in size_list:
    if int(i) <= 20:
        area_room_size_dict['1-20㎡']+=1
    elif  20 < int(i) <= 40:
        area_room_size_dict['20-40㎡']+=1
    elif int(i) > 40:
        area_room_size_dict['40㎡以上']+=1

#  各区域房源数量（柱状图-纵向）
def area_house_num() -> Bar:
    c = (
        Bar(init_opts=opts.InitOpts(width="600px", height="300px"))
        .add_xaxis(list(area_num_dict.keys()))
        .add_yaxis("数量", list(area_num_dict.values()))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="武汉房源数量", subtitle="武汉各地区房源数量"),
            xaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(rotate=30)
            )
        )
    )
    return c

#  各区域房源的平均价（折线图）
def area_house_average_price() -> Line:
    c = (
        Line(init_opts=opts.InitOpts(width="600px", height="300px"))
        .add_xaxis(list(average_price_dict.keys()))
        .add_yaxis("平均价", list(average_price_dict.values()))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="武汉房源平均价", subtitle="武汉各地区房源平均价"),
            xaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(rotate=30)
            )
        )
    )
    return c

#  各区域房源户型数量（柱状图-横向）
def area_house_type_num() -> Bar:
    c = (
        Bar(init_opts=opts.InitOpts(width="600px", height="300px"))
        .add_xaxis(list(area_room_type_dict.keys()))
        .add_yaxis("数量", list(area_room_type_dict.values()))
        .reversal_axis()
        .set_series_opts(label_opts=opts.LabelOpts(position="right"))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="武汉房源户型数量", subtitle="武汉各地区房源户型数量"),
        )
    )
    return c

#  各区域房源面积区间占比（饼图）
def area_room_size() -> Pie:
    c = (
        Pie(init_opts=opts.InitOpts(width="600px", height="335px"))
        .add("", [list(z) for z in zip(area_room_size_dict.keys(), area_room_size_dict.values())])
        .set_global_opts(title_opts=opts.TitleOpts(title="武汉房源面积占比"))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        ) 
    return c

#  汇集所有图标
def page_simple_layout():
    #  page = Page()   默认布局
    page = Page(layout=Page.SimplePageLayout)
    page.add(
        area_house_num(),
        area_house_average_price(),
        area_house_type_num(),
        area_room_size()
    )
    page.render("贝壳租房.html")

page_simple_layout()
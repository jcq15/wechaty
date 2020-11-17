import pandas as pd
import requests
from bs4 import BeautifulSoup


class WeatherForecaster:
    def __init__(self, abs_path='/home/wechat/wechatbot/'):
        self.abs_path = abs_path
        self.source_file = self.abs_path + 'resources/weather_city_id.csv'
        self.source_url = 'http://www.weather.com.cn/weather/'
        self.city_id = pd.read_csv(self.source_file, encoding='gbk')

    def get_weather(self, city):
        li = list(self.city_id[self.city_id['城市'] == city]['citycode'])

        if not li:
            return '没这地儿！'
        else:
            str_id = str(li[0])

            ui = self.source_url + str_id + '.shtml'
            ri = requests.get(url=ui)  # 访问页面
            ri.encoding = ri.apparent_encoding  # encoding

            soup = BeautifulSoup(ri.text, 'html.parser')
            #ul_tag = soup.find('ul', 't clearfix')
            body1 = soup.body  # 获取body部分
            data = body1.find('div', {'id': '7d'})  # 找到id为7d的div
            ul = data.find('ul')  # 获取ul部分
            li = ul.find_all('li')  # 获取所有的li
            final = city + '7日天气速递：\n'

            for day in li:  # 对每个li标签中的内容进行遍历

                data = day.find('h1').string  # 找到日期
                temp = '【' + data + '】'

                inf = day.find_all('p')  # 找到li中的所有p标签
                if inf[1].find('span') is None:
                    temperature_highest = '无'  # 天气当中可能没有最高气温（傍晚）
                else:
                    temperature_highest = inf[1].find('span').string  # 找到最高气温
                    temperature_highest = temperature_highest
                temperature_lowest = inf[1].find('i').string  # 找到最低温
                temperature_lowest = temperature_lowest  # 最低温度后面有个℃，去掉这个符号

                temp += inf[0].string + '   '
                temp += '最高:' + str(temperature_highest) + '   '
                temp += '最低:' + str(temperature_lowest) + '\n'
                final += temp

            return final

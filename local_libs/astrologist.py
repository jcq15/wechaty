import requests
from bs4 import BeautifulSoup


class Astrologist:
    def __init__(self):
        self.xz_cn_to_eng = {
        '狮子座': 'leo',
        '金牛座': 'taurus',
        '白羊座': 'aries',
        '双子座': 'gemini',
        '巨蟹座': 'cancer',
        '处女座': 'virgo',
        '天秤座': 'libra',
        '天蝎座': 'scorpio',
        '射手座': 'sagittarius',
        '摩羯座': 'capricorn',
        '水瓶座': 'aquarius',
        '双鱼座': 'pisces'}

        self.source_url = 'https://www.xzw.com/fortune/'

    def get_data(self, xz):
        if xz not in self.xz_cn_to_eng:
            return '这是什么星座啊，我不认识！'
        else:
            xz_en = self.xz_cn_to_eng[xz]
            url = self.source_url + xz_en + '/'
            ri = requests.get(url=url)  # 访问页面
            # ri.encoding = ri.apparent_encoding  # encoding
            soupi = BeautifulSoup(ri.text, 'lxml')  # 解析页面
            infor1 = soupi.find('div', class_="c_main").find('ul').find_all('li')
            infor2 = soupi.find('div', class_="c_cont").find_all('p')

            res = '你是可爱的' + xz + '宝宝！\n'

            for i in range(4):
                star_c = int(infor1[i].find('em')['style'].split(':')[1].split('p')[0]) // 16
                str_tmp = '【' + infor1[i].text[:-1] + '】' + star_c * '★' + (5 - star_c) * '☆' + '\n'
                str_txt = infor2[i].find('span').text + '\n'
                res = res + str_tmp + str_txt

            for i in range(4, 10):
                print(infor1[i])
                print(infor1[i].find('label').text)
                print(infor1[i].text.split('：'))
                str_tmp = '【' + infor1[i].find('label').text[:-1] + '】' + infor1[i].text.split('：')[-1] + '\n'
                if i == 4:
                    str_tmp = str_tmp + infor2[i].find('span').text + '\n'

                res = res + str_tmp

            return res

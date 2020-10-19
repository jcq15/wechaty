import datetime
import json
import logging
import random
import math
import itertools
import numpy as np
import re
from pypinyin import pinyin, Style
import requests
from bs4 import BeautifulSoup
import pandas as pd

'''这样记录日志
logger.info('This is a log info')
logger.debug('Debugging')
logger.warning('Warning exists')
'''
logging.basicConfig(level=logging.DEBUG, filename='/home/wechat/wechatbot/output.log')
logger = logging.getLogger(__name__)

# 成语接龙的管理者
class cyjl_server:
    data = []               # 成语们，简单粗暴

    def __init__(self):   
        self.now = ''       # 当前成语
        self.index = 0      # 第几个词
        self.scores = {}    # 大家的分数，字典，key为user_id，value是list，第一个是分数，第二个是昵称
        self.result = []    # 可以接的词
        if len(cyjl_server.data) == 0:
            with open("/home/wechat/wechatbot/cyjl.txt", "r") as f:
                counter = 0
                for line in f:
                    content = line.split("\t")
                    #word = content[0]
                    #pinyin = content[1].split("'")
                    #meaning = content[2].replace("\n", "")
                    cyjl_server.data.append(content[0])
                    counter += 1
            logger.info("Init finished! [%d] words." % (counter))
        self.start()

    # 开始
    def start(self):
        while True:
            word = random.sample(cyjl_server.data, 1)[0]
            print(word[-1])
            result = self.get_start_with(word[-1])
            if result:       # 后继有人
                self.result = result
                self.now = word
                print(self.now)
                self.index = 1
                return True

    # 以某个字开头的成语们
    def get_start_with(self, last_word):
        result = [word for word in cyjl_server.data if pinyin(word, style=Style.NORMAL)[0][0] in pinyin(last_word, style=Style.NORMAL)[0]]
        return result

    # 某人发了个开头正确的消息，接受正义的审判吧
    def judge(self, answer, username, nickname):
        if answer in self.result:    # 这该死的群友，数理基础竟然如此扎实
            self.index += 1
            self.now = answer
            if username in self.scores:   # 已经有了，+1，没有则增加
                self.scores[username][0] += 1
            else:
                self.scores[username] = [1,nickname]
            self.result = self.get_start_with(answer[-1])
            return True
        return False

    # 游戏结束
    def end_game(self):
        # 成绩排序
        items=self.scores.items()
        backitems=[v[1] for v in items]      # 分数，昵称
        backitems.sort()

        reply = '本次共接龙了%s轮，大家的成绩为：\n' % (self.index-1)
        for backitem in backitems:
            reply += '%s:%s分\n' % (backitem[1], backitem[0])
        return reply

class Baoshi:
    def __init__(self):
        
        self.model = r'frog2.0启动！淦！已经\h点\m分了！你今天学习了吗？'
        self.function = '我是青蛙！我有这些功能，都要@我噢！\n'\
                           '1. 发送“功能”查看功能；\n'\
                           '2. 发送“报时”报时；\n'\
                           '3. 发送“24点”，给你四个数算24点。一定能算出来，算不出来说明你是傻逼；\n'\
                           '4. 发送“48点”，给你四个数算48点。一定能算出来，算不出来说明你是大傻逼；\n'\
                           '5. 发送“计算 表达式”进行计算，例如“计算 114000+514”;\n'\
                           '6. 发送“天气 城市”进行计算，例如“天气 北京”;\n'\
                           '7. 发送“今日运势 星座”进行算命，例如“今日运势 狮子座”'
        self.status = 0           # 0: 无状态, 'cyjl': 在玩成语接龙

    # 获取报时内容
    def gettext(self):
        response_text = ''
        status = False
        for c in self.model:
            if not status:
                if c == chr(92):
                    status = True
                else:
                    response_text += c
            else:
                status = False
                if c == chr(92):
                    response_text += c
                elif c == 'h':
                    response_text += str(datetime.datetime.now().hour)
                elif c == 'm':
                    response_text += str(datetime.datetime.now().minute)
                elif c == 's':
                    response_text += str(datetime.datetime.now().second)
                else:
                    pass
        return response_text

    def __infix_evaluator(self, infix_expression : str):
        '''这是中缀表达式求值的函数
        :参数 infix_expression:中缀表达式
        '''
        def get_value(operator : str, op1 : int, op2 : int):
            '''这是四则运算函数
            :参数 operator:运算符
            :参数 op1:左边的操作数
            :参数 op2:右边的操作数
            '''
            if operator == '+':
                return op1 + op2
            elif operator == '-':
                return op1 - op2
            elif operator == '*':
                return op1 * op2
            elif operator == '/':
                return op1 / op2
        infix_expression = infix_expression.replace('（', '(').replace('）', ')').replace(' ', '')
        token_list = re.split("([+-/\*\(\)])", infix_expression)
        print(token_list)
        # 运算符优先级字典
        pre_dict = {'*':3,'/':3,'+':2,'-':2,'(':1}
        # 运算符栈
        operator_stack = []
        # 操作数栈
        operand_stack = []
        for token in token_list:
            if not token:
                continue
            # 数字进操作数栈
            if token.isdecimal() or token[1:].isdecimal():
                operand_stack.append(int(token))
            # 左括号进运算符栈
            elif token == '(':
                operator_stack.append(token)
            # 碰到右括号，就要把栈顶的左括号上面的运算符都弹出求值
            elif token == ')':
                top = operator_stack.pop()
                while top != '(':
                    # 每弹出一个运算符，就要弹出两个操作数来求值
                    # 注意弹出操作数的顺序是反着的，先弹出的数是op2
                    op2 = operand_stack.pop()
                    op1 = operand_stack.pop()
                    # 求出的值要压回操作数栈
                    # 这里用到的函数get_value在下面有定义
                    operand_stack.append(get_value(top,op1,op2))
                    # 弹出下一个栈顶运算符
                    top = operator_stack.pop()
            # 碰到运算符，就要把栈顶优先级不低于它的都弹出求值
            elif token in '+-*/':
                while operator_stack and pre_dict[operator_stack[-1]] >= pre_dict[token]:
                    top = operator_stack.pop()
                    op2 = operand_stack.pop()
                    op1 = operand_stack.pop()
                    operand_stack.append(get_value(top,op1,op2))
                # 别忘了最后让当前运算符进栈
                operator_stack.append(token)
        # 表达式遍历完成后，栈里剩下的操作符也都要求值   
        while operator_stack:
            top = operator_stack.pop()
            op2 = operand_stack.pop()
            op1 = operand_stack.pop()
            operand_stack.append(get_value(top,op1,op2))
        # 最后栈里只剩下一个数字，这个数字就是整个表达式最终的结果
        return operand_stack[0]
     
    def handle(self, data):
        # AB学习时间！
        if data['contact'].name == 'AB':
            return ('要期中考试了还水群呢？？', 'mention')

        if data['mentionSelf']:
            text = data['text'].replace('@青蛙 ', '').replace('@青蛙\u2005', '')
            userid = data['contact'].id
            usernick = data['contact'].name


            if self.status == 'cyjl':
                if text == '结束成语接龙':             # 结束
                    reply = self.cyjl.end_game()
                    self.status = 0
                    self.cyjl = None
                    return reply
                elif text == '成语接龙':               # 成语接龙
                    return '你是不是沙雕，我们已经在玩成语接龙了！当前是第%s个成语：\n【%s】' % (self.cyjl.index, self.cyjl.now)
                elif text == '要看答案':
                    return ', '.join(self.cyjl.result)
                elif len(text) == 4:                 # 响应所有四字信息
                    if self.cyjl.judge(text, userid, usernick):             # 还真接上了
                        reply = '恭喜%s接龙成功！当前是第%s个成语：\n【%s】' % (usernick, self.cyjl.index, self.cyjl.now)
                        if 0 == len(self.cyjl.result):                 # 后面没法接
                            reply += '\n这成语没法接，算了，就玩到这吧！\n' + self.cyjl.end_game()
                            self.status = 0
                            self.cyjl = None
                        return reply
                    else:   # 没接上
                        return '%s，不对不对！你说的什么玩意，【%s】不是成语！' % (usernick, text)
                
            if len(text) >= 6 and text[:4] == '修改模板':
                self.model = text[5:]
                return '修改成功！现在的模板是：\n' + self.model

            elif text == '功能':
                return self.function

            elif text == '报时':
                return self.gettext()

            elif len(text) >= 4 and text[:2] == '计算':
                _, expression = text.split(' ')
                return str(self.__infix_evaluator(text[3:]))

            elif text == 'ping':
                return str(data['age'])

            elif text == '24点':
                num_list = []    
                array_data = np.loadtxt('/home/wechat/wechatbot/24p_1_9.txt')
                len(list(array_data))
                id=np.random.randint(low=0, high=len(list(array_data)))
                choice = list(array_data)[id]
                choice = [int(c) for c in choice]
                num_str_list = [str(c) for c in choice]
                res = ' '.join(num_str_list)
                return '4 numbers:' + res

            elif text == '48点':
                num_list = []    
                array_data = np.loadtxt('/home/wechat/wechatbot/48p_1_13.txt')
                len(list(array_data))
                id=np.random.randint(low=0, high=len(list(array_data)))
                choice = list(array_data)[id]
                choice = [int(c) for c in choice]
                num_str_list = [str(c) for c in choice]
                res = ' '.join(num_str_list)
                return '4 numbers:' + res
            
            # 未上线的今日星座运势功能
            elif len(text) >= 4 and text[:4] == '今日运势':
                def get_data(ui, xz):
                    ri = requests.get(url = ui)   # 访问页面
                    ri.encoding = ri.apparent_encoding # encoding
                    soupi = BeautifulSoup(ri.text, 'lxml')  # 解析页面
                    infor1 = soupi.find('div',class_="c_main").find('ul').find_all('li')
                    infor2 = soupi.find('div',class_="c_cont").find_all('p')
                    
                    res = '你是可爱的' + xz + '宝宝！\n'
                    for i in range(4):
                        star_c = int(infor1[i].find('em')['style'].split(':')[1].split('p')[0]) // 16
                        str_tmp = '【' + infor1[i].text[:-1] + '】'  +  star_c * '★' + (5-star_c) * '☆' + '\n'
                        str_txt = infor2[i].find('span').text + '\n'
                        res = res + str_tmp + str_txt
                        
                    for i in range(4,10):
                        str_tmp = '【' + infor1[i].find('label').text[:-1] + '】'+ infor1[i].text.split('：')[1] + '\n'
                        if i == 4: str_tmp = str_tmp + infor2[i].find('span').text + '\n'
                        res = res + str_tmp

                    return res
                xz_cn_to_eng = {
                                '狮子座':'leo',
                                '金牛座':'taurus',
                                '白羊座':'aries',
                                '双子座':'gemini',
                                '巨蟹座':'cancer',
                                '处女座':'virgo',
                                '天秤座':'libra',
                                '天蝎座':'scorpio',
                                '射手座':'sagittarius',
                                '摩羯座':'capricorn',
                                '水瓶座':'aquarius',
                                '双鱼座':'pisces'}       
                _, xz = text.split(' ')
                xz_eg = xz_cn_to_eng[xz]
                url = 'https://www.xzw.com/fortune/' + xz_eg + '/'
                res = get_data(url, xz)
                #print(res)
                return res

            elif len(text) >= 4 and text[:5] == '晚安小青蛙':
                return '你是猪吗？还睡！别@我了，再@自杀！'


            elif len(text) >= 4 and text[:2] == '天气':
                _, city = text.split(' ')
                city_id = pd.read_csv('/home/wechat/wechatbot/weather_city_id.csv',encoding='gbk')
                def get_weather(city):
                    str_id = str(list(city_id[city_id['城市']==city]['citycode'])[0])
                    ui = 'http://www.weather.com.cn/weather/' + str_id + '.shtml'
                    ri = requests.get(url = ui)   # 访问页面
                    ri.encoding = ri.apparent_encoding # encoding

                    soup = BeautifulSoup(ri.text, 'html.parser')
                    ul_tag = soup.find('ul', 't clearfix')
                    body1 = soup.body  # 获取body部分
                    data = body1.find('div', {'id': '7d'})  # 找到id为7d的div
                    ul = data.find('ul')  # 获取ul部分
                    li = ul.find_all('li')  # 获取所有的li
                    final = city + '7日天气速递：\n'

                    for day in li:   # 对每个li标签中的内容进行遍历

                        data = day.find('h1').string   # 找到日期
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
                res  = get_weather(city)
                return res


            # 未正式上线的测试功能
            elif text == '测试图片':
                return ('/home/wechat/wechatbot/images/testimg.png', 'image')

            elif self.status == 0 and text == '成语接龙':             # 结束
                self.cyjl = cyjl_server()
                self.status = 'cyjl'
                return '成语接龙开始！当前是第%s个成语：\n%s' % (self.cyjl.index, self.cyjl.now)

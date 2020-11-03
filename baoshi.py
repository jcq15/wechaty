from local_libs.cyjl_server import CYJLServer
from local_libs.gif_generator import GIFGenerator
from local_libs.time_reporter import TimeReporter
from local_libs.astrologist import Astrologist
from local_libs.weather_forecaster import WeatherForecaster
import numpy as np
import random
from pypinyin import pinyin, Style

from local_libs import safe_calculation as sc
import uuid


class Baoshi:
    def __init__(self):
        self.abs_path = '/home/wechat/wechatbot/'
        self.prob_threshold = 0.1
        self.cyjl = CYJLServer()
        self.time_reporter = TimeReporter()
        self.astrologist = Astrologist()
        self.weather_forecaster = WeatherForecaster()
        self.gif_generator = GIFGenerator()
        self.function = '@我并发送括号里的内容就行噢！\n' \
                        '1. 【功能】\n' \
                        '2. 【报时】\n' \
                        '3. 【24点】或【48点】\n' \
                        '4. 【运行 code】运行python代码，例如【运行 [i*i for i in range(10)]】\n' \
                        '5. 【天气 城市】查询天气，例如【天气 北京】\n' \
                        '6. 【今日运势 星座】算命，例如【今日运势 狮子座】\n' \
                        '7. 【成语接龙】，例如【成语接龙】\n' \
                        '8. 【种田】 你田了!\n' \
                        '9. 【再种一次田】\n'

        self.status = 0  # 0: 无状态, 'cyjl': 在玩成语接龙

    def cyjl_helper(self, data, text):
        userid = data['contact'].id
        usernick = data['contact'].name

        if text == '结束成语接龙':  # 结束
            reply = self.cyjl.end_game()
            self.status = 0

            return reply

        elif text == '成语接龙':  # 成语接龙
            return '你是不是沙雕，我们已经在玩成语接龙了！当前是第%s个成语：\n【%s】' % (self.cyjl.index, self.cyjl.now)
        elif text == '要看答案':
            return self.cyjl.report_solutions()
        elif len(text) > 0 and self.cyjl.data[self.cyjl.now][-1] in pinyin(text, style=Style.NORMAL)[0]:  # 第一个字对上了
            reply = self.cyjl.judge(text, userid, usernick)

            if not self.cyjl.next_list:  # 后面没法接
                reply += '\n这成语没法接，算了，就玩到这吧！\n' + self.cyjl.end_game()
                self.status = 0
            else:
                pass

            return reply
        else:
            return '我们玩成语接龙呢，你少来插嘴没用的！'

    def handle(self, data):
        # # AB学习时间！
        # if data['contact'].name == 'Kris_AB':
        #     return '小乖乖快去学习啦！别水群了！！！'

        # return str(data)

        if data['mentionSelf']:
            text = data['text'].replace('@青蛙 ', '').replace('@青蛙\u2005', '')


            if self.status == 0 and text == '成语接龙':  # 结束
                self.status = 'cyjl'
                self.cyjl.start()
                return '成语接龙开始！当前是第%s个成语：\n%s' % (self.cyjl.index, self.cyjl.now)

            elif len(text) >= 6 and text[:4] == '修改模板':
                self.time_reporter.set_template(text[5:])
                return '修改成功！现在的模板是：\n' + self.time_reporter.template

            elif text == '功能':
                return self.function

            elif text == '报时':
                return self.time_reporter.gettext()

            elif len(text) >= 3 and text[:2] == '计算' or text[:2] == '运行':
                expression = text[2:]
                res = sc.safe_calculate(expression.lstrip(), 2)
                print(res)
                return res

            elif text == 'ping':
                return str(data['age'])

            elif text == '24点':
                array_data = np.loadtxt(self.abs_path + 'resources/24p_1_9.txt')
                ind = np.random.randint(low=0, high=len(list(array_data)))
                choice = list(array_data)[ind]
                choice = [int(c) for c in choice]
                num_str_list = [str(c) for c in choice]
                res = ' '.join(num_str_list)
                return '4 numbers: ' + res

            elif text == '48点':
                array_data = np.loadtxt(self.abs_path + 'resources/48p_1_13.txt')
                ind = np.random.randint(low=0, high=len(list(array_data)))
                choice = list(array_data)[ind]
                choice = [int(c) for c in choice]
                num_str_list = [str(c) for c in choice]
                res = ' '.join(num_str_list)
                return '4 numbers: ' + res

            # 今日星座运势功能
            elif len(text) >= 4 and text[:4] == '今日运势':
                return self.astrologist.get_data(text)

            elif len(text) >= 4 and text[:5] == '晚安小青蛙':
                return '你是猪吗？还睡！别@我了，再@自杀！'

            elif len(text) >= 4 and text[:2] == '天气':
                _, city = text.split(' ')
                return self.weather_forecaster.get_weather(city)

            # 未正式上线的测试功能
            elif text == '测试图片':
                return self.abs_path + 'resources/images/testimg.png', 'image'

            elif len(text) >= 5 and text[:3] == 'gif':
                content = text[4:]
                filename = self.abs_path + 'resources/images/' + str(uuid.uuid1()) + '.gif'
                self.gif_generator.create_gif(content, filename=filename)

                return filename, 'image'

            elif self.status == 'cyjl':
                return self.cyjl_helper(data, text)
            else:
                return '本蛙懒得理你！'
        else:
            if random.random() < self.prob_threshold:
                return '本蛙不说话就静静看你们聊天！'
            else:
                return None

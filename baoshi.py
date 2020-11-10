from local_libs.cyjl_server import CYJLServer
from local_libs.gif_generator import GIFGenerator
from local_libs.time_reporter import TimeReporter
from local_libs.astrologist import Astrologist
from local_libs.weather_forecaster import WeatherForecaster
from local_libs import calculator
from local_libs import PyOJAgent
from local_libs.latex_delegate import LaTeXDelegate
from local_libs.sudoku_manager import SudokuManager

import numpy as np
import random
import re
from pypinyin import pinyin, Style

import uuid


class Baoshi:
    def __init__(self):
        self.abs_path = '/home/wechat/wechatbot/'
        # self.abs_path = 'D:/bot_local/wechatbot/'
        self.prob_threshold = 0.2
        self.status = 0  # 0: 无状态, 'cyjl': 在玩成语接龙
        self.cyjl = CYJLServer(abs_path=self.abs_path)
        self.time_reporter = TimeReporter()
        self.astrologist = Astrologist()
        self.weather_forecaster = WeatherForecaster(abs_path=self.abs_path)

        self.oj_agent = PyOJAgent.PyOJAgent()
        self.oj_in_progress = False
        self.latex_color_str = '000000'
        self.gif_fg_color_str = '660874'
        self.gif_bg_color_str = 'ffffff'
        self.gif_generator = GIFGenerator(
            fg_color='#' + self.gif_fg_color_str,
            bg_color='#' + self.gif_bg_color_str)
        self.latex_resolution = 600
        self.latex_delegate = LaTeXDelegate()
        self.sudoku_manager = SudokuManager()
        self.function = '@我并发送【括号】里的内容就行噢！\n' \
                        '0. 【功能】\n' \
                        '1. 【报时】\n' \
                        '2. 【24点】或【48点】\n' \
                        '3. 【运行 code】运行python代码，例如【运行 [i*i for i in range(10)]】\n' \
                        '4. 【天气 城市】查询天气，例如【天气 北京】\n' \
                        '5. 【今日运势 星座】算命，例如【今日运势 狮子座】\n' \
                        '6. 【成语接龙】，例如【成语接龙】\n' \
                        '7. 【OJ 题号】 做OJ题目，例如 【OJ 2】\n' \
                        '8. 【提交OJ 代码】 提交OJ代码，例如【提交OJ def main_function(a, b): return a + b】\n' \
                        '9. 【latex 表达式】 由LaTeX表达式生成图片，例如【latex e^{i\\pi} + 1 = 0】\n' \
                        'A. 【latex颜色 6位色号(RRGGBB)】 修改LaTeX颜色，例如【颜色 114514】\n' \
                        'B. 【分辨率 数值】 修改LaTeX分辨率，例如【分辨率 600】\n' \
                        'C. 【gif 文本】 由文本生成gif图片，例如【gif 苟利国家生死以】\n'\
                        'D. 【gif前景色 6位色号(RRGGBB)】 修改gif前景色，例如【gif前景色 660874】\n' \
                        'E. 【数独】 显示当前数独题目，例如【数独】\n'\
                        'F. 【数独 重新出题】 出一道新数独题，例如【数独 重新出题】\n'\
                        '10. 【数独 rcn】 在当前数独第r行第c列填入数字n，行列范围均为1-9，例如【数独 123】\n'\
                        '11. 【数独 答案】 显示当前数独答案，例如【数独 答案】\n'
                        # 'E. 【gif背景色 6位色号(RRGGBB)】 修改gif背景色，例如【gif背景色 123456】\n'

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

    @staticmethod
    def parse_text(text):
        main_arg = None
        other_arg = None

        segs = text.split()

        if len(segs) > 0:
            main_arg = segs[0]

            if len(segs) > 1:
                other_arg = segs[1]
            else:
                pass
        else:
            pass

        return main_arg, other_arg

    def handle(self, data):

        if data['mentionSelf']:
            text = data['text'].replace('\u2005', '')
            text = text.replace('@青蛙', '')
            text = text.lstrip()

            main_arg, other_arg = self.parse_text(text)

            if not main_arg:
                return '不说话就别撩我！'
            else:
                pass

            if self.status == 0 and main_arg == '成语接龙':  # 结束
                self.status = 'cyjl'
                self.cyjl.start()
                return '成语接龙开始！当前是第%s个成语：\n%s' % (self.cyjl.index, self.cyjl.now)

            elif other_arg and main_arg == '修改模板':
                self.time_reporter.set_template(other_arg)
                return '修改成功！现在的模板是：\n' + self.time_reporter.template

            elif main_arg == '功能':
                return self.function

            elif main_arg == '报时':
                return self.time_reporter.gettext()

            elif other_arg and (main_arg == '计算' or main_arg == '运行'):
                expression = text[2:]
                res = calculator.safe_calculate(expression.lstrip(), 2)
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
            elif other_arg and main_arg == '今日运势':
                return self.astrologist.get_data(other_arg)

            elif len(text) >= 5 and text[:5] == '晚安小青蛙':
                return '你是猪吗？还睡！别@我了，再@自杀！'

            elif other_arg and main_arg == '天气':
                return self.weather_forecaster.get_weather(other_arg)

            elif other_arg and main_arg.lower() == 'oj':
                try:
                    problem_id = int(other_arg)
                except ValueError as e:
                    # print(repr(e))
                    return '请输入合法的题号！'
                else:
                    oj_filename = self.abs_path + 'resources/OJ/Problems/Problem' + str(problem_id) + '.plm'
                    success = self.oj_agent.load_problem_file(oj_filename)

                    if not success:
                        return '田了！题库里没这题！'
                    else:
                        return self.oj_agent.describe_problem()

            elif other_arg and main_arg.lower() == '提交oj':
                if self.oj_in_progress:
                    return '上一个OJ还没测试完呢，先等会儿！急什么！'
                else:
                    self.oj_in_progress = True
                    code = text[4:].lstrip()
                    self.oj_agent.test_submission(code)
                    self.oj_in_progress = False

                    return self.oj_agent.report_submission_result()

            elif main_arg.lower() == 'latex':
                expression = text[5:].lstrip()
                filename = self.abs_path + 'resources/images/' + str(uuid.uuid1()) + '.png'

                status, info = self.latex_delegate.latex2png(
                    expression=expression, local_file_name=filename,
                    resolution=self.latex_resolution, color_str=self.latex_color_str
                )

                if status:
                    return info, 'image'
                else:
                    return info
            elif main_arg == 'latex颜色':
                if len(other_arg) == 6 and re.match(r'[0-9a-fA-F]{6}', other_arg):
                    self.latex_color_str = other_arg
                    return 'LaTeX颜色修改成功！当前颜色为：' + other_arg.lower()
                else:
                    return '别胡闹，没这色儿！'
            elif main_arg == '分辨率':
                try:
                    res = int(other_arg)

                    if 1 <= res <= 1000:
                        self.latex_resolution = res
                        return '分辨率修改成功！当前分辨率为：{0}'.format(res)
                    else:
                        return '分辨率过大或过小！'
                except Exception as e:
                    return '分辨率必须是正整数！'

            elif main_arg == '数独':
                filename = self.abs_path + 'resources/images/' + str(uuid.uuid1()) + '.jpg'

                if not other_arg:
                    if not self.sudoku_manager.problem:
                        self.sudoku_manager.generate()
                        self.sudoku_manager.generate_image(filename=filename, option='problem')
                    else:
                        self.sudoku_manager.generate_image(filename=filename, option='user')

                    return filename, 'image'

                elif other_arg == '重新出题':
                    self.sudoku_manager.generate()
                    self.sudoku_manager.generate_image(filename=filename, option='problem')
                    return filename, 'image'
                elif other_arg == '答案':
                    if not self.sudoku_manager.problem:
                        return '题都没有，哪来的答案！'
                    else:
                        self.sudoku_manager.generate_image(filename=filename, option='answer')
                        return filename, 'image'
                else:
                    if len(other_arg) == 3 and re.match(r'[1-9]{2}[0-9]{1}', other_arg):
                        row = int(other_arg[0]) - 1
                        col = int(other_arg[1]) - 1
                        num = int(other_arg[2])
                        result = self.sudoku_manager.user_fill(row, col, num)

                        if not result[0]:
                            return result[1]
                        else:
                            if result[1].lower() == 'Finished':
                                print('完成！')
                            else:
                                print('未完成！')

                            self.sudoku_manager.generate_image(filename=filename, option='user')

                            return filename, 'image'
                    else:
                        return '输入不合法！'

            elif main_arg.lower() == 'gif前景色':
                if len(other_arg) == 6 and re.match(r'[0-9a-fA-F]{6}', other_arg):
                    self.gif_fg_color_str = other_arg
                    self.gif_generator.fg_color = '#' + self.gif_fg_color_str
                    return 'gif前景色修改成功！当前颜色为：' + other_arg.lower()
                else:
                    return '别胡闹，没这色儿！'

            # 未正式上线的测试功能
            elif main_arg.lower() == 'gif背景色':
                if len(other_arg) == 6 and re.match(r'[0-9a-fA-F]{6}', other_arg):
                    self.gif_bg_color_str = other_arg
                    self.gif_generator.bg_color = '#' + self.gif_bg_color_str
                    return 'gif背景色修改成功！当前颜色为：' + other_arg.lower()
                else:
                    return '别胡闹，没这色儿！'

            elif text == '测试图片':
                return self.abs_path + 'resources/images/testgif.gif', 'image'

            elif len(text) >= 5 and text[:3] == 'gif':
                content = text[4:]
                filename = self.abs_path + 'resources/images/' + str(uuid.uuid1()) + '.gif'
                self.gif_generator.create_gif(content, filename=filename)

                return filename, 'image'

            elif self.status == 'cyjl':
                return self.cyjl_helper(data, text)
            else:
                if random.random() < self.prob_threshold:
                    return '本蛙懒得理你！'
                else:
                    return None
        else:
            if random.random() < self.prob_threshold:
                return '本蛙不说话就静静看你们聊天！'
            else:
                return None

import logging
import random
from pypinyin import pinyin, Style


# 成语接龙的管理者
class CYJLServer:
    def __init__(self, abs_path='/home/wechat/wechatbot/', word_dict=None):
        self.abs_path = abs_path
        self.word_dict = {}  # 成语们，简单粗暴

        self.now = ''       # 当前成语
        self.index = 0      # 第几个词
        self.scores = {}    # 大家的分数，字典，key为user_id，value是list，第一个是分数，第二个是昵称
        self.next_list = []    # 可以接的词
        self.used = []
        self.activated = False
        logging.basicConfig(level=logging.DEBUG, filename=self.abs_path + 'output.log')
        self.logger = logging.getLogger(__name__)

        '''这样记录日志
        logger.info('This is a log info')
        logger.debug('Debugging')
        logger.warning('Warning exists')
        '''

        if not word_dict:
            with open(self.abs_path + "resources/coal_dict.txt", "r", encoding='utf-8') as f:
                counter = 0
                for line in f:
                    content = line.split("\t")
                    # print(content)
                    #word = content[0]
                    #pinyin = content[1].split("'")
                    content[6] = content[6].replace("\n", "")
                    if not content[6] in self.word_dict:
                        self.word_dict[content[6]] = (content[3].split(' '))[:-1]
                        counter += 1

            self.logger.info("Init finished! [%d] words." % counter)
        else:
            self.word_dict = word_dict

    def is_active(self):
        return self.activated

    def is_plausible_candidate(self, cand_str):     # cand_str第一个字能不能接上当前最后一个字
        if not self.now or not self.is_active():
            return False
        else:
            return self.word_dict[self.now][-1] in pinyin(cand_str[0], style=Style.NORMAL, v_to_u=True, heteronym=True)[0]

    def get_status(self):
        return '当前是第{0}个成语：\n{1}'.format(self.index, self.now)

    # 开始
    def start(self):
        self.scores = {}  # 大家的分数，字典，key为user_id，value是list，第一个是分数，第二个是昵称
        self.next_list = []  # 可以接的词
        self.used = []
        self.activated = True

        while True:
            word = random.sample(self.word_dict.keys(), 1)[0]
            # print(word)
            # print(word[-1])
            result = self.get_start_with(word)
            if result:       # 后继有人
                self.next_list = result
                self.now = word
                self.used.append(word)
                print(self.now)
                self.index = 1

                return True
            else:
                continue

    # 以某个字开头的成语们
    def get_start_with(self, last_word):
        result = [word for word in self.word_dict
                  if self.word_dict[word][0] == self.word_dict[last_word][-1] and word not in self.used]
        # result = [word for word in cyjl_server.data if pinyin(word, style=Style.NORMAL)[0][0] in pinyin(last_word, style=Style.NORMAL)[0]]
        return result

    # 某人发了个开头正确的消息，接受正义的审判吧
    def judge(self, answer, username, nickname):
        if answer in self.used:
            return '你个辣鸡，这个成语接过了！'
        elif answer in self.next_list:    # 这该死的群友，数理基础竟然如此扎实
            self.now = answer
            self.used.append(answer)
            self.index += 1
                
            if username in self.scores:   # 已经有了，+1，没有则增加
                self.scores[username][0] += 1
            else:
                self.scores[username] = [1, nickname]

            reply = '恭喜%s接龙成功！当前是第%s个成语：\n【%s】' % (nickname, self.index, self.now)
            self.next_list = self.get_start_with(answer)

            if not self.next_list:
                reply += '\n这成语没法接，算了，就玩到这吧！\n' + self.cyjl.end_game()
            else:
                pass
            return reply
        else:
            return '%s，不对不对！你说的什么玩意，【%s】接不上！' % (nickname, answer)

    def report_solutions(self):
        return ', '.join(self.next_list)

    # 游戏结束
    def end_game(self):
        # 成绩排序
        self.activated = False
        items = self.scores.items()
        backitems = [v[1] for v in items]      # 分数，昵称
        backitems.sort(reverse=True)

        reply = '本次共接龙了%s轮，大家的成绩为：\n' % (self.index - 1)

        for backitem in backitems:
            reply += '%s:%s分\n' % (backitem[1], backitem[0])

        reply += '接龙回顾：\n'

        for word in self.used:
            reply += word + ' '

        return reply

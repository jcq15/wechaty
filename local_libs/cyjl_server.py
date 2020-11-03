import logging
import random


# 成语接龙的管理者
class CYJLServer:
    def __init__(self):
        self.abs_path = '/home/wechat/wechatbot/'
        self.data = {}  # 成语们，简单粗暴
        self.now = ''       # 当前成语
        self.index = 0      # 第几个词
        self.scores = {}    # 大家的分数，字典，key为user_id，value是list，第一个是分数，第二个是昵称
        self.next_list = []    # 可以接的词
        self.used = set()
        logging.basicConfig(level=logging.DEBUG, filename=self.abs_path + 'output.log')
        self.logger = logging.getLogger(__name__)

        '''这样记录日志
        logger.info('This is a log info')
        logger.debug('Debugging')
        logger.warning('Warning exists')
        '''

        with open(self.abs_path + "resources/coal_dict.txt", "r", encoding='gbk') as f:
            counter = 0
            for line in f:
                content = line.split("\t")
                #word = content[0]
                #pinyin = content[1].split("'")
                content[2] = content[2].replace("\n", "")
                if not content[2] in self.data:
                    self.data[content[2]] = (content[1].split(' '))[:-1]
                    counter += 1
        self.logger.info("Init finished! [%d] words." % counter)

    # 开始
    def start(self):
        self.scores = {}  # 大家的分数，字典，key为user_id，value是list，第一个是分数，第二个是昵称
        self.next_list = []  # 可以接的词
        self.used = set()

        while True:
            word = random.sample(self.data.keys(), 1)[0]
            print(word[-1])
            result = self.get_start_with(word)
            if result:       # 后继有人
                self.next_list = result
                self.now = word
                self.used.add(word)
                print(self.now)
                self.index = 1

                return True
            else:
                continue

    # 以某个字开头的成语们
    def get_start_with(self, last_word):
        result = [word for word in self.data if self.data[word][0] == self.data[last_word][-1]]
        # result = [word for word in cyjl_server.data if pinyin(word, style=Style.NORMAL)[0][0] in pinyin(last_word, style=Style.NORMAL)[0]]
        return result

    # 某人发了个开头正确的消息，接受正义的审判吧
    def judge(self, answer, username, nickname):
        if answer in self.next_list:    # 这该死的群友，数理基础竟然如此扎实
            if answer in self.used:
                return '你个辣鸡，这个成语接过了！'
            else:
                self.used.add(answer)
                self.index += 1
                self.now = answer

                if username in self.scores:   # 已经有了，+1，没有则增加
                    self.scores[username][0] += 1
                else:
                    self.scores[username] = [1, nickname]

                self.next_list = self.get_start_with(answer)
                reply = '恭喜%s接龙成功！当前是第%s个成语：\n【%s】' % (nickname, self.index, self.now)
                return reply
        else:
            return '%s，不对不对！你说的什么玩意，【%s】接不上！' % (nickname, answer)

    def report_solutions(self):
        return ', '.join(self.next_list)

    # 游戏结束
    def end_game(self):
        # 成绩排序
        items = self.scores.items()
        backitems = [v[1] for v in items]      # 分数，昵称
        backitems.sort()

        reply = '本次共接龙了%s轮，大家的成绩为：\n' % (self.index-1)
        for backitem in backitems:
            reply += '%s:%s分\n' % (backitem[1], backitem[0])

        return reply

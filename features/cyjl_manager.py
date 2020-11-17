from features.feature_manager import ReflectiveManager
from local_libs.cyjl_server import CYJLServer


class CYJLManager(ReflectiveManager):
    def __init__(self):
        super().__init__(private_enabled=False)
        self.user_config = {}
        self.word_dict = {}

        with open(self.abs_path + "resources/coal_dict.txt", "r", encoding='utf-8') as f:
            counter = 0
            for line in f:
                content = line.split("\t")
                content[6] = content[6].replace("\n", "")
                if not content[6] in self.word_dict:
                    self.word_dict[content[6]] = (content[3].split(' '))[:-1]
                    counter += 1

    def reflective_handle(self, data) -> list:
        args, _ = self.preprocess(data)
        recipient = ReflectiveManager.get_source(data)
        userid = data['contact'].id
        usernick = data['contact'].name

        if not args:
            return self.make_null_response()
        else:
            if not self.user_config.get(recipient):
                self.user_config[recipient] = CYJLServer(word_dict=self.word_dict)
            else:
                pass

            server = self.user_config[recipient]
            msg = None

            if args[0] == '结束成语接龙' and server.is_active():
                msg = server.end_game()
            elif args[0] == '成语接龙':
                if server.is_active():
                    msg = '你是不是沙雕，我们已经在玩成语接龙了！' + server.get_status()
                else:
                    server.start()
                    msg = '成语接龙开始！' + server.get_status()
            elif args[0] == '要看答案':
                if server.is_active():
                    msg = server.report_solutions()
                else:
                    msg = '没答案，看什么看！'
            elif server.is_plausible_candidate(args[0]):  # 第一个字对上了
                msg = server.judge(args[0], userid, usernick)
            else:
                pass

            if msg:
                return ReflectiveManager.reply_text(msg, data, with_mention=True)
            else:
                return ReflectiveManager.make_null_response()

from datetime import datetime as dt
from features.feature_manager import ReflectiveManager
from features.response_message import ResponseMessage


class SelfIntroManager(ReflectiveManager):
    def __init__(self):
        super().__init__()
        self.config_file = self.abs_path + 'resources/self_intro.txt'
        self.version = '3.14159'
        self.template = 'frog {0}启动！淦！已经{1}点{2}分{3}秒了！你今天学习了吗？'
        self.description = '读取描述文件失败！'

        with open(self.config_file, 'r') as f:
            self.description = f.read()

    def reflective_handle(self, data) -> list:
        args, _ = self.preprocess(data)

        if not args:
            return self.make_null_response()
        else:
            if args[0] == '功能':
                return self.reply_text(self.description, data)
            elif args[0] == '报时':
                return self.reply_text(self.template.format(self.version,
                        dt.now().hour, dt.now().minute, dt.now().second
                ), data, with_mention=True)
            elif args[0].startswith('晚安小青蛙'):
                return self.reply_text('晚安么么哒mua~\U0001f497\ufe0f', data, with_mention=True)
            elif args[0].lower() == 'ping':
                return self.reply_text(str(data['age']), data, with_mention=True)
            else:
                return self.make_null_response()



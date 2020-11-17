from features.feature_manager import ReflectiveManager


class MingyuanManager(ReflectiveManager):
    def __init__(self):
        super().__init__(private_enabled=False)

    def reflective_handle(self, data) -> list:
        print(data['contact'].name)

        if data['contact'].name == 'tensorspace':
            msg = '闭嘴吧张量空间，本机器人看不下去了！'
            return self.reply_text(msg, data, with_mention=True)
        else:
            return self.make_null_response()



from features.response_message import ResponseMessage
import math
import uuid


class FeatureManager:

    TEXT_LIMIT = 5000   # 16384英文或5461中文，保险起见留出余量
    SEG_LIMIT = 20      # 单条上限，防止过度刷屏
    ABS_PATH = None

    with open('bot_abs_path.txt', 'r') as f:
        ABS_PATH = f.readline().rstrip()

    def __init__(self, nickname='青蛙'):
        self.nickname = nickname
        self.abs_path = FeatureManager.ABS_PATH
        self.feature = '抽象功能'



    # main method to be override for specific features
    def handle(self, data) -> list:
        return self.make_null_response()

    # ===================== Helper Methods ============================

    def preprocess(self, data):
        text = data['text'].replace('\u2005', '')
        text = text.replace('@' + self.nickname, '')
        text = text.lstrip()
        args = text.split()

        if args:
            text = text.replace(args[0], '', 1)
            text.lstrip()
        else:
            pass
        
        return args, text

    def report(self):
        print('nickname: {0}, feature: {1}'.format(self.nickname, self.feature))

    @staticmethod
    def make_image_response(filename, recipients=None) -> list:
        return [ResponseMessage(message_type='image', content=filename,
                                recipients=recipients)]

    @staticmethod
    def make_text_response(text, recipients=None, mentions=None) -> list:

        text_length = len(text)

        if text_length <= FeatureManager.TEXT_LIMIT:
            return [ResponseMessage(message_type='text', content=text,
                                    recipients=recipients, mentions=mentions)]
        else:
            hard_limit = FeatureManager.TEXT_LIMIT * FeatureManager.SEG_LIMIT

            if text_length > hard_limit:
                name = str(uuid.uuid1()) + '.txt'
                filename = FeatureManager.ABS_PATH + 'resources/overlength_texts/' + name
                with open(filename, 'w') as f:
                    f.write(text)

                msg = '消息过长无法直接显示，请见以下文件：\n' + name
                resp1 = [ResponseMessage(message_type='text', content=msg,
                                         recipients=recipients, mentions=mentions)]
                resp2 = FeatureManager.make_image_response(filename, recipients=recipients)

                return resp1 + resp2
            else:
                current_ind = 0
                segs = []
                seg_num = math.ceil(text_length / FeatureManager.TEXT_LIMIT)
                counter = 1

                while current_ind < text_length:
                    upper = min(text_length, current_ind + FeatureManager.TEXT_LIMIT)
                    head = '消息过长，自动切分：【{0}/{1}】\n'.format(counter, seg_num)
                    segs.append(head + text[current_ind: upper])
                    current_ind += FeatureManager.TEXT_LIMIT
                    counter += 1

                return [ResponseMessage(message_type='text', content=seg,
                                        recipients=recipients, mentions=mentions)
                        for seg in segs]

    @staticmethod
    def make_null_response() -> list:
        return ResponseMessage.make_null_list()


# 谁发就回谁，可群可私（星座，24点，48点，报时，天气，LaTeX，gif，自我介绍）
# 可选择性关闭对私聊的响应（数独，成/田语接龙）
class ReflectiveManager(FeatureManager):
    def __init__(self, public_enabled=True, private_enabled=True):
        super().__init__()
        self.feature = '反射式功能'
        self.public_enabled = public_enabled
        self.private_enabled = private_enabled

    def handle(self, data) -> list:
        if data['roomid']:
            if self.public_enabled:
                return self.reflective_handle(data)
            else:
                return self.make_null_response()
        else:
            if self.private_enabled:
                return self.reflective_handle(data)
            else:
                return self.make_null_response()

    # main method to be override for specific features
    def reflective_handle(self, data) -> list:
        return self.make_null_response()

    # ======================= HELPERS ==========================

    @staticmethod
    def get_source(data):
        if data['roomid']:
            return data['roomid']
        else:
            return data['contact'].id

    @staticmethod
    def reply_image(filename, data) -> list:
        recipient = ReflectiveManager.get_source(data)

        return ReflectiveManager.make_image_response(
            filename, recipients=[recipient])

    @staticmethod
    def reply_text(text, data, with_mention=False) -> list:
        recipient = ReflectiveManager.get_source(data)

        if data['roomid']:
            mentions = [data['contact'].id] if with_mention else None
            
            return ReflectiveManager.make_text_response(
                text, recipients=[recipient], mentions=mentions)
        else:
            return ReflectiveManager.make_text_response(
                text, recipients=[recipient])


# 需要综合群聊与私聊的信息实现复杂功能（阿瓦隆，投票）
class ComprehensiveManager(FeatureManager):
    def __init__(self):
        super().__init__()
        self.feature = '综合功能'


# 无情的转发机器
class ForwardingManager(FeatureManager):
    def __init__(self):
        super().__init__()
        self.feature = '反射式功能'
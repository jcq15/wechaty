import features
from features.feature_manager import FeatureManager
from features.response_message import ResponseMessage
from features.self_intro_manager import SelfIntroManager
from features.twenty_four_manager import TwentyFourManager
from features.latex_manager import LaTeXManager
from features.weather_manager import WeatherManager
from features.astrology_manager import AstrologyManager
from features.gif_manager import GIFManager
from features.sudoku_manager import SudokuManager
from features.calculator_manager import CalculatorManager
from features.oj_manager import OJManager
from features.cyjl_manager import CYJLManager
from features.mingyuan_manager import MingyuanManager
import random


class MessageDistributor:
    def __init__(self):
        self.room_list = [
            '22043367685@chatroom',     # 0 原生报时群
            '17488219531@chatroom',     # 1 青蛙测试群
            '23360500993@chatroom',     # 2 大雾群
            '18208220357@chatroom',     # 3 qingwa测试
            '22225182752@chatroom',     # 4 文理工青蛙文学洞
            '4309278385@chatroom',      # 5 python交流群
            '14700918607@chatroom',     # 6 春季直播群
            '714388336@chatroom',       # 7 雷锋
            '21717572132@chatroom',     # 8 JHU
            '5610951052@chatroom',      # 9 开花
            '6478156134@chatroom',      # 10 108
            '23871291939@chatroom',     # 11 zijing
            '20850370374@chatroom',     # 12 mingyuan


        ]

        self.reflective_managers = [
            SelfIntroManager(),
            TwentyFourManager(),
            LaTeXManager(),
            WeatherManager(),
            AstrologyManager(),
            GIFManager(),
            SudokuManager(),
            CalculatorManager(),
            OJManager(),
            CYJLManager(),
        ]

        self.public_manager_map = {key: self.reflective_managers.copy()
                            for key in self.room_list[:11]}

        self.public_manager_map[self.room_list[-1]] = [MingyuanManager()]

        self.private_managers = self.reflective_managers.copy()

        # to be used
        self.comprehensive_managers = []

    def handle_input_data(self, data) -> list:
        responses = []
        room_id = data['roomid']

        if room_id:
            if room_id in self.public_manager_map:
                for manager in self.public_manager_map[room_id]:
                    current_response_list = manager.handle(data)

                    if ResponseMessage.is_null_list(current_response_list):
                        continue
                    else:
                        responses += current_response_list
            else:
                return [ResponseMessage(
                    message_type='text', content='青蛙在本群未注册功能！',
                    recipients=[room_id])]
        else:
            for manager in self.private_managers:
                current_response_list = manager.handle(data)

                if ResponseMessage.is_null_list(current_response_list):
                    continue
                else:
                    responses += current_response_list

        if responses and not ResponseMessage.is_null_list(responses):
            return responses
        else:   # 全是田功能
            recipients = [room_id] if room_id else [data['contact'].id]
            men = 'wxid_nyz3zh795amf22'
            if room_id == self.room_list[5]:
                msg = '什么别的网网友，什么之前一个好好友？你讲清楚点行吗？上来就哈哈哈问你是谁又不说你莫不是有毛病我要真认识你我能没有你好友？你要真认识群里不好意思，我忘了你不会自己加我？拍来拍去的问半天说了个P'
                return [ResponseMessage(
                    message_type='text', content=msg, recipients=recipients, mentions=[men])]

            elif random.random() < 0.2:

                return [ResponseMessage(message_type='text',
                                        content='本蛙就静静看着你们！', recipients=recipients)]
            else:
                return [ResponseMessage()]







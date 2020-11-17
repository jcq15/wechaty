from features.feature_manager import ReflectiveManager
from features.response_message import ResponseMessage
import numpy as np


class TwentyFourManager(ReflectiveManager):
    def __init__(self):
        super().__init__()
        self.file24 = self.abs_path + 'resources/24p_1_9.txt'
        self.file48 = self.abs_path + 'resources/48p_1_13.txt'

        self.data24 = np.loadtxt(self.file24)
        self.data48 = np.loadtxt(self.file48)

    def reflective_handle(self, data) -> list:
        args, _ = self.preprocess(data)

        if not args:
            return self.make_null_response()
        else:
            if args[0] == '24点':
                ind = np.random.randint(low=0, high=len(list(self.data24)))
                choice = list(self.data24)[ind]
                choice = [int(c) for c in choice]
                num_str_list = [str(c) for c in choice]
                res = ' '.join(num_str_list)
                text = '4 numbers: ' + res
                return self.reply_text(text, data, with_mention=True)
            elif args[0] == '48点':
                ind = np.random.randint(low=0, high=len(list(self.data48)))
                choice = list(self.data48)[ind]
                choice = [int(c) for c in choice]
                num_str_list = [str(c) for c in choice]
                res = ' '.join(num_str_list)
                text = '4 numbers: ' + res
                return self.reply_text(text, data, with_mention=True)
            else:
                return self.make_null_response()



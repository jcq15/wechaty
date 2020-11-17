from features.feature_manager import ReflectiveManager
from local_libs import calculator


class CalculatorManager(ReflectiveManager):
    def __init__(self):
        super().__init__()
        self.time_limit_in_seconds = 2

    def reflective_handle(self, data) -> list:
        args, text = self.preprocess(data)

        if not args:
            return self.make_null_response()
        else:
            if args[0] == '计算' or args[0] == '运行':
                expression = text
                res = calculator.safe_calculate(expression.lstrip(), self.time_limit_in_seconds)
                msg = '【运行结果】\n' + res
                return ReflectiveManager.reply_text(msg, data, with_mention=True)
            else:
                return self.make_null_response()



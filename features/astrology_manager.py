from features.feature_manager import ReflectiveManager
from local_libs.astrologist import Astrologist


class AstrologyManager(ReflectiveManager):
    def __init__(self):
        super().__init__()
        self.astrologist = Astrologist()

    def reflective_handle(self, data) -> list:
        args, _ = self.preprocess(data)

        if not args or len(args) < 2:
            return self.make_null_response()
        else:
            if args[0] == '今日运势':
                xz = args[1]
                msg = self.astrologist.report(xz)
                return self.reply_text(msg, data, with_mention=True)
            else:
                return self.make_null_response()



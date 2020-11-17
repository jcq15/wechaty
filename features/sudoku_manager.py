from features.feature_manager import ReflectiveManager
from local_libs.sudoku_delegate import SudokuDelegate
import uuid
import re


class SudokuManager(ReflectiveManager):
    def __init__(self):
        super().__init__()
        self.user_config = {}

    def reflective_handle(self, data) -> list:
        args, text = self.preprocess(data)
        recipient = ReflectiveManager.get_source(data)

        if not args:
            return self.make_null_response()
        else:
            if args[0] == '数独':
                filename = self.abs_path + 'resources/images/' + str(uuid.uuid1()) + '.jpg'

                if not self.user_config.get(recipient):
                    self.user_config[recipient] = SudokuDelegate()
                else:
                    pass

                delegate = self.user_config[recipient]

                if len(args) == 1:
                    if not delegate.problem:
                        delegate.generate()
                        delegate.generate_image(filename=filename, option='problem')
                    else:
                        delegate.generate_image(filename=filename, option='user')

                    return ReflectiveManager.reply_image(filename, data)

                elif args[1] == '重新出题':
                    delegate.generate()
                    delegate.generate_image(filename=filename, option='problem')

                    return ReflectiveManager.reply_image(filename, data)

                elif args[1] == '答案':
                    if not delegate.problem:
                        msg = '题都没有，哪来的答案！'

                        return ReflectiveManager.reply_text(msg, data, with_mention=True)
                    else:
                        delegate.generate_image(filename=filename, option='answer')

                        return ReflectiveManager.reply_image(filename, data)

                elif len(args[1]) == 3 and re.match(r'[1-9]{2}[0-9]{1}', args[1]):
                    row = int(args[1][0]) - 1
                    col = int(args[1][1]) - 1
                    num = int(args[1][2])
                    result = delegate.user_fill(row, col, num)

                    if not result[0]:
                        return ReflectiveManager.reply_text(result[1], data, with_mention=True)
                    else:
                        if result[1].lower() == 'finished':
                            msg = '数独题目已正确解答！恭喜！'
                        else:
                            msg = '数独题目尚未成功解答！加油继续努力！'

                        resp1 = ReflectiveManager.reply_text(msg, data, with_mention=True)
                        delegate.generate_image(filename=filename, option='user')

                        return resp1 + ReflectiveManager.reply_image(filename, data)
                else:
                    msg = '数独：输入不合法！'

                    return ReflectiveManager.reply_text(msg, data, with_mention=True)
            else:
                return self.make_null_response()


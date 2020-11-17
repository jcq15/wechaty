from features.feature_manager import ReflectiveManager
from features.response_message import ResponseMessage
from local_libs.latex_delegate import LaTeXDelegate
import uuid
import re

class LaTeXManager(ReflectiveManager):
    def __init__(self):
        super().__init__()
        self.latex_delegate = LaTeXDelegate()
        self.default_resolution = 600
        self.default_color = '000000'
        self.user_config = {'default': [self.default_resolution, self.default_color]}

    def reflective_handle(self, data) -> list:
        args, text = self.preprocess(data)
        recipient = ReflectiveManager.get_source(data)

        if not args or len(args) < 2:
            return self.make_null_response()
        else:
            if args[0].lower() == 'latex':
                expression = text
                filename = self.abs_path + 'resources/images/' + str(uuid.uuid1()) + '.png'

                resolution, color = self.user_config.get(recipient, self.user_config['default'])

                status, info = self.latex_delegate.latex2png(
                    expression=expression, local_file_name=filename,
                    resolution=resolution, color_str=color
                )

                if status:
                    return self.reply_image(info, data)
                else:
                    return self.reply_text(info, data, with_mention=True)
            elif args[0].lower() == 'latex颜色':
                if len(args[1]) == 6 and re.match(r'[0-9a-fA-F]{6}', args[1]):
                    args[1] = args[1].lower()
                    if recipient in self.user_config:
                        self.user_config[recipient][1] = args[1]
                    else:
                        self.user_config[recipient] = [self.default_resolution, args[1]]

                    msg = 'LaTeX颜色修改成功！当前颜色为：' + args[1]

                    return self.reply_text(msg, data)
                else:
                    msg = '别胡闹，没这色儿！'
                    return self.reply_text(msg, data, with_mention=True)
            elif args[0].lower() == '分辨率':
                msg = 'Resolution?'
                try:
                    res = int(args[1])

                    if 1 <= res <= 1000:
                        if recipient in self.user_config:
                            self.user_config[recipient][0] = res
                        else:
                            self.user_config[recipient] = [res, self.default_color]

                        msg = '分辨率修改成功！当前分辨率为：{0}'.format(res)
                    else:
                        msg = '分辨率过大或过小！'
                except Exception as e:
                    msg = '分辨率必须是正整数！'
                    print(repr(e))
                finally:
                    return self.reply_text(msg, data, with_mention=True)
            else:
                return self.make_null_response()



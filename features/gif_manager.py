from features.feature_manager import ReflectiveManager
from local_libs.gif_generator import GIFGenerator
import uuid
import re


class GIFManager(ReflectiveManager):
    def __init__(self):
        super().__init__()
        self.gif_generator = GIFGenerator()
        self.default_resolution = 600
        self.default_fg_color = '660874'
        self.default_bg_color = 'ffffff'
        self.user_config = {'default': [self.default_fg_color, self.default_bg_color]}
        self.gif_generator.set_fg(self.default_fg_color)
        self.gif_generator.set_bg(self.default_bg_color)

    def reflective_handle(self, data) -> list:
        args, text = self.preprocess(data)
        recipient = ReflectiveManager.get_source(data)

        if not args or len(args) < 2:
            return self.make_null_response()
        else:
            if args[0].lower() == 'gif':
                filename = self.abs_path + 'resources/images/' + str(uuid.uuid1()) + '.gif'
                fg_color, bg_color = self.user_config.get(recipient, self.user_config['default'])
                self.gif_generator.set_fg(fg_color)
                self.gif_generator.set_bg(bg_color)
                self.gif_generator.create_gif(text, filename=filename)

                return ReflectiveManager.reply_image(filename, data)

            elif args[0].lower() == 'gif前景色':
                if len(args[1]) == 6 and re.match(r'[0-9a-fA-F]{6}', args[1]):
                    args[1] = args[1].lower()
                    if recipient in self.user_config:
                        self.user_config[recipient][0] = args[1]
                    else:
                        self.user_config[recipient] = [args[1], self.default_bg_color]

                    msg = 'gif前景色修改成功！当前颜色为：' + args[1]

                    return self.reply_text(msg, data)
                else:
                    msg = '别胡闹，没这色儿！'

                    return self.reply_text(msg, data, with_mention=True)

            elif args[0].lower() == 'gif背景色':   # temporarily hidden
                if len(args[1]) == 6 and re.match(r'[0-9a-fA-F]{6}', args[1]):
                    args[1] = args[1].lower()
                    if recipient in self.user_config:
                        self.user_config[recipient][1] = args[1]
                    else:
                        self.user_config[recipient] = [self.default_fg_color, args[1]]

                    msg = 'gif背景色修改成功！当前颜色为：' + args[1]

                    return self.reply_text(msg, data)
                else:
                    msg = '别胡闹，没这色儿！'
                    return self.reply_text(msg, data, with_mention=True)
            else:
                return self.make_null_response()



import datetime


class TimeReporter:
    def __init__(self):
        self.template = r'frog3.14启动！淦！已经\h点\m分了！你今天学习了吗？'

    def set_template(self, txt):
        self.template = txt

    # 获取报时内容
    def gettext(self):
        response_text = ''
        status = False
        for c in self.template:
            if not status:
                if c == chr(92):
                    status = True
                else:
                    response_text += c
            else:
                status = False
                if c == chr(92):
                    response_text += c
                elif c == 'h':
                    response_text += str(datetime.datetime.now().hour)
                elif c == 'm':
                    response_text += str(datetime.datetime.now().minute)
                elif c == 's':
                    response_text += str(datetime.datetime.now().second)
                else:
                    pass

        return response_text

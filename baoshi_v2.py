import datetime
import json

name = '2020毕业热爱'
model = r'淦！已经\h点\m分了！你今天学习了吗？'

# 获取报时内容
def gettext():
    response_text = ''
    status = False
    for c in model:
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


def handle(data):
    global model
    text = data['text']
    if len(text) >= 6 and text[:4] == '修改模板':
        model = text[5:]
        return json.dumps({'type': 'text', 'content': '修改大成功！现在的模板是：\n'+model})
    elif text == '报时':
        return json.dumps({'type': 'text', 'content': gettext()})
    else:
        return json.dumps({'type': 'null'})

import datetime
import json
name = '2020毕业热爱'
model = r'frog2.0启动！淦！已经\h点\m分了！你今天学习了吗？'

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
        return json.dumps({'type': 'text', 'content': '修改成功！现在的模板是：\n'+model})
    elif text == '报时':
        return json.dumps({'type': 'text', 'content': gettext()})
    elif len(text) >= 4  and text[:2] == '加法':
        add1 = text.split(' ')[1]
        add2 = text.split(' ')[2]
        try:
            answer = int(add1) + int(add2)
            return json.dumps({'type': 'text', 'content': '算好了哦!答案是: '+str(answer)})
        except:
            return json.dumps({'type': 'text', 'content': '淦！你给我的是啥?'})
    
    elif len(text) >= 4  and text[:2] == '乘法':
        add1 = text.split(' ')[1]
        add2 = text.split(' ')[2]
        try:
            answer = float(add1) * float(add2)
            return json.dumps({'type': 'text', 'content': '算好了哦!答案是: '+str(answer)})
        except:
            return json.dumps({'type': 'text', 'content': '淦！你给我的是啥?'})
    else:
        return json.dumps({'type': 'null'})


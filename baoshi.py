import datetime
import json

name = '2020毕业热爱'
model = '淦！已经h点m分了！你今天学习了吗？'

def handle(data):
    global model
    text = data['text']
    if len(text) >= 6 and text[:4] == '修改模板':
        model = text[5:]
        return json.dumps({'type': 'text', 'content': '修改大成功！现在的模板是：\n'+model})
    elif text == '报时':
        response_text = model.replace('h', str(datetime.datetime.now().hour)).replace('m', str(datetime.datetime.now().minute))
        print(json.dumps({'type': 'text', 'content': response_text}))
        return json.dumps({'type': 'text', 'content': response_text})
    else:
        return json.dumps({'type': 'null'})

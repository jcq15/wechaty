import datetime
import json
import logging
import random
import math
import itertools

logging.basicConfig(level=logging.DEBUG, filename='/home/wechat/wechatbot/output.log')
logger = logging.getLogger(__name__)

'''这样记录日志
logger.info('This is a log info')
logger.debug('Debugging')
logger.warning('Warning exists')
'''

logger.info('helloworld')

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


def judgePoint24(nums):
    if len(nums) == 1:
        return math.isclose(nums[0], 24)
    return any(judgePoint24([x] + rest)
                for a, b, *rest in itertools.permutations(nums)
                for x in {a+b, a-b, a*b, b and a/b})


def handle(data):
    if data['mentionSelf']:
        global model
        text = data['text'].replace('@青蛙 ', '')
        text = text.replace('@青蛙\u2005', '')

        # 测试开始
        #return json.dumps({'type': 'text', 'content': eval(text)})
        # 测试结束

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
        
        elif text == '24点':
            num_list = []    
            for i in range(4):
                num_list.append(str(random.randint(1,9)))
                res = ' '.join(num_list)
            return json.dumps({'type':'text','content':'4 numbers:'+res})

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
    else:
        return json.dumps({'type': 'null'})


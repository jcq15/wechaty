import traceback
from message_distributor import MessageDistributor
from features import ResponseMessage
from flask import Flask
from flask import request
import json
import datetime
import logging
import io
import sys
sys.path.append('../../home/wechat/wechatbot/')

import baoshi               # 报时群
import baoshitest           # 报时测试
import mingyuan

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

### Setup the console handler with a StringIO object
log_capture_string = io.StringIO()
ch = logging.StreamHandler(log_capture_string)
ch.setLevel(logging.DEBUG)

### Add the console handler to the logger
log.addHandler(ch)


# 全局变量

groups = {
    '22043367685@chatroom': baoshi.Baoshi(),     # 原生报时群
    '17488219531@chatroom': baoshi.Baoshi(),     # 青蛙测试群
    '23360500993@chatroom': baoshi.Baoshi(),     # 大雾群
    '18208220357@chatroom': baoshi.Baoshi(),     # qingwa测试
    '22225182752@chatroom': baoshi.Baoshi(),     # 文理工青蛙文学洞
    '4309278385@chatroom': baoshi.Baoshi(),      # python交流群
    '14700918607@chatroom': baoshi.Baoshi(),     # 春季直播群
    '714388336@chatroom': baoshi.Baoshi(),       # 雷锋
    '21717572132@chatroom': baoshi.Baoshi(),     # JHU
}

message_distributor = MessageDistributor()

# 待完善，房间类
class Room():
    def __init__(self, topic=''):
        self.topic = topic

# 待完善，联系人类
class Contact():
    def __init__(self, _id='', name='', friend=False):
        self.id = _id
        self.name = name
        self.friend = friend

class Message():
    # 传入的date是字符串
    def __init__(self, *, text='', room_topic='', date=''):
        self.text = text
        if room_topic:
            self.room = Room(room_topic)
        else:
            self.room = None
        #if date:
        #    self.date = 

'''
mmutableMultiDict([('text', '@青蛙 '), ('roomtopic', '2020毕业热爱wуkkm 图灵测试群'), ('roomid', '22043367685@chatroom'), ('date', '"2020-09-22T10:22:10.884Z"'), 
('contactid', 'wxid_4qznf9kshn6z22'), 
('contactname', '给我也整一个'), 
('contactfriend', 'true'), 
('mentions', '[{"domain":null,"_events":{},"_eventsCount":0,"id":"wxid_x0dlfz5rhn7y22","payload":{"alias":"","avatar":"http://wx.qlogo.cn/mmhead/ver_1/X6Lw8cRmBpmib2H6m4O4gv2yboOF7ibyicHNTD6icUQRjaKu0BbcJNrYbk3VQ0sOAm6ibDLPNtlJAVDqdjojUc9jMicDfyMx6fjk8MZwV6AN6FBsg/0","city":"","friend":true,"gender":0,"id":"wxid_x0dlfz5rhn7y22","name":"青蛙","phone":[],"province":"","signature":"","type":1,"weixin":"shadiao_bot"}}]'),
 ('mentionSelf', 'true'), ('age', '1')])
'''

def handle(good_data):
    if good_data['roomid']:     # 是群
        roomid = good_data['roomid']
        if roomid == '23871291939@chatroom':
            response = zijing.handle(good_data)
        elif roomid == '20850370374@chatroom':
            response = mingyuan.handle(good_data)
        elif roomid in groups:
            response = groups[roomid].handle(good_data)
        else:
            response = ''
        #print(response)
        if not response:
            return json.dumps([{'type': 'null'}])
        # 回复
        if isinstance(response, str):
            return json.dumps([{'type': 'text', 'content': response}])
        elif isinstance(response, tuple):
            return json.dumps([{'type': response[1], 'content': response[0]}])
        else:
            return json.dumps([{'type': 'null'}])

    else:
        #resp_list[0] = json.dumps({'type': 'null'})
        return json.dumps([{'type': 'null'}])


@app.route('/message', methods=['GET', 'POST'])
def message():
    try:
        if request.method == 'POST':
            data = request.form
            good_data = {
                'text': data['text'],
                'roomtopic': data['roomtopic'],
                'roomid': data['roomid'],
                'date': datetime.datetime.strptime(data['date'][:-6], '"%Y-%m-%dT%H:%M:%S'), #"2020-09-22T10:22:10.884Z"
                'contact': Contact(_id=data['contactid'], name=data['contactname'], friend=bool(data['contactfriend'])),
                'mentions': [Contact(_id=m['id'], name=m['payload']['name'], friend=m['payload']['friend']) for m in json.loads(data['mentions'])],
                'mentionSelf': data['mentionSelf']=='true',
                'age': float(data['age']),
            }
            print(good_data)
            print(good_data['contact'].id)#, good_data['contact'].name)
            resp = message_distributor.handle_input_data(good_data)
            return ResponseMessage.list_to_json(resp)
            resp = handle(good_data)
            return resp if resp else json.dumps([{'type': 'null'}])
        return json.dumps([{'type': 'null'}])
    except Exception as ee:
        #log.exception(ee)
        #log_contents = log_capture_string.getvalue()
        #log_capture_string.close()
        print(ee)
        traceback.print_exc()
        return json.dumps([{'type':'text', 'content':'对不起，我出错了！呜呜呜！联系管理员解决吧！'}])


# 返回当前报时内容
@app.route('/clock', methods=['GET'])
def clock():
    return baoshi_admin.gettext()

if __name__ == '__main__':
    app.run(debug=True)

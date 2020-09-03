from flask import Flask
from flask import request
import json
import datetime

import zijing               # 学校相关服务（私用）
import baoshi               # 报时群

app = Flask(__name__)


# 全局变量



# 待完善，房间类
class Room():
    def __init__(self, topic=''):
        self.topic = topic

# 待完善，联系人类
class Contact():
    def __init__(self, id=''):
        self.id = id

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


@app.route('/message', methods=['GET', 'POST'])
def message():
    if request.method == 'POST':
        data = request.form
        print(data)
        roomtopic = data['roomtopic']
        if roomtopic:     # 是群
            if roomtopic == zijing.name:
                return zijing.handle(data)
            # 报时群
            elif len(roomtopic) >= 8 and roomtopic[0:8] == baoshi.name:
                return baoshi.handle(data)                
    return json.dumps({'type':'null'})


# 返回当前报时内容
@app.route('/clock', methods=['GET'])
def clock():
    return baoshi.model.replace('h', str(datetime.datetime.now().hour)).replace('m', str(datetime.datetime.now().minute))



if __name__ == '__main__':
    app.run()

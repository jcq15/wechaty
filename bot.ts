// bot.ts
import { Contact, Message, Wechaty } from 'wechaty'
import { ScanStatus } from 'wechaty-puppet'
import { PuppetPadplus } from 'wechaty-puppet-padplus'
import QrcodeTerminal from 'qrcode-terminal'
import { FileBox }  from 'wechaty'
import { my_token }  from './password'

const token = my_token

const puppet = new PuppetPadplus({
  token,
})

const name  = 'shadiao_bot'

const bot = new Wechaty({
  name: 'shadiao_bot',
  puppet, // generate xxxx.memory-card.json and save login data for the next login
})

/*
//报时器，已经废弃不用，但这里定时任务的写法可能以后有用
async function hourReport() {
    //当前时间
    var time = new Date();
    //小时
    var hours = time.getHours();
    //分钟
    var mins = time.getMinutes();
    //秒钟
    var secs = time.getSeconds();
    //下一次报时间隔
    var next = ((60 - mins) * 60 - secs) * 1000;
    //设置下次启动时间
    setTimeout(hourReport, next);
    //整点报时，因为第一次进来mins可能不为0所以要判断
    const room = await bot.Room.find({topic:baoshi})
    
    var request = require('request')
    request.get({url:'http://127.0.0.1:5000/clock'}, function (error, response, body) {  
        if (error) {
            console.log('Error :', error)
            return
        }
        console.log(' Body :', body)
        if(body.length > 0){
          room?.say(body)
        }
    })
}
*/


bot.on('scan', (qrcode, status) => {
    if (status === ScanStatus.Waiting) {
      QrcodeTerminal.generate(qrcode, {
        small: true
      })
    }
  })
bot.on('login', async (user: Contact) => {
    console.log(`login success, user: ${user}`)
    /*
    //查找群
    const room = await bot.Room.find({topic: baoshi}) // change `event-room` to any room topic in your wechat
    if (room) {
      room.on('topic', (room, topic, oldTopic, changer) => {
        console.log(`Room topic changed from ${oldTopic} to ${topic} by ${changer.name()}`)
      })
    }
    */
    //启动报时器
    //hourReport();
  })
bot.on('message', async (msg: Message) => {
    console.log(`msg : ${msg}`)
    var room = msg.room()
    var topic = ''
    var r_id = ''
    if(room){
      topic = await room.topic()
      r_id = room.id
    }
    var contact = msg.from()
    var mention_self = await msg.mentionSelf()
    var mention_list = await msg.mentionList()
    //console.log(contact?.id)
    //console.log(contact?.name())
    //console.log(contact?.friend())

    //原地回复的直接推给python处理，我们获得回复内容
    var request = require('request')
    var base64js = require('base64-js')
    var formData = {
      text: msg.text(),
      roomtopic: topic,
      roomid: r_id,
      date: JSON.stringify(msg.date()),
      
      contactid: contact?.id,
      contactname: contact?.name(),
      contactfriend: String(contact?.friend()),  //是否是好友

      //contacttype: contact?.type(),   //获取好友的类型，是公众号还是普通
      //contactgender: contact?.gender(),
      //isGroup: msg.isGroup(),
      //isSelf: msg.self(),
      
      mentions: JSON.stringify(mention_list),
      mentionSelf: String(mention_self),
      age: String(msg.age()),
    }
    try{
    // 所有的东西都推到后端用python处理
    request.post({url:'http://127.0.0.1:5000/message', formData: formData}, async function (error, response, body) {  
        if (error) {
            console.log('Error :', error)
            return
        }
        var response = JSON.parse(body)
        console.log(response)
        if(body.length > 0){
          const type: string = response['type']
          if(type=='image'){
            const path: string = response['content']

            const fs = require('fs');
            const contents = fs.readFileSync(path, {encoding: 'base64'});
            // Example call:
            
              const filebox_b64 = FileBox.fromBase64(contents, path)
              if(room){
                console.log('准备发啦！')
                room.say(filebox_b64)
              }else{
                contact?.say(filebox_b64)
              }
            

          }
          if(type=='images'){
            const path: string[] = response['content']
            console.log(path)
            for(let p of path){
              const filebox: FileBox = FileBox.fromFile(p)
              if(room){
                console.log('准备发啦！')
                room.say(filebox)
              }else{
                contact?.say(filebox)
              }
            }
          }else if(type=='text'){
            const text: string = response['content']
            if(room){
              room.say(text)
            }else{
              contact?.say(text)
            }
          }else if(type=='mention'){
            if(room){
              room.say(response['content'], contact)
            }
          }else{
            //什么也不做呗
          }     
        }
    })
  }catch(e){
    console.log(e)
  }
  })
bot.start()
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


//var baoshimodel = `淦！已经${hours}点了！你今天学习了吗？`
var baoshi: RegExp = new RegExp('2020毕业热爱.*')
//var baoshimodel = '淦！已经h点m分了！你今天学习了吗？'

//报时器
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
    hourReport();
  })
bot.on('message', async (msg: Message) => {
    console.log(`msg : ${msg}`)
    var room = msg.room()
    var topic = ''
    if(room){
      topic = await room.topic()
    }
    var contact = msg.from()

    //原地回复的直接推给python处理，我们获得回复内容
    var request = require('request')
    var formData = {
      text: msg.text(),
      roomtopic: topic,
      date: JSON.stringify(msg.date()),
      contactid: contact?.id,
    }
    try{
      // 所有的东西都推到后端用python处理
      request.post({url:'http://127.0.0.1:5000/message', formData: formData}, function (error, response, body) {  
          if (error) {
              console.log('Error :', error)
              return
          }
          console.log(' Body :', body)
          var response = JSON.parse(body)
          if(body.length > 0){
            const type: string = response['type']
            if(type=='image'){
              const path: string = response['content']
              const filebox: FileBox = FileBox.fromFile(path)
              if(room){
                console.log('准备发啦！')
                room.say(filebox)
              }else{
                contact?.say(filebox)
              }
            }else if(type=='text'){
              const text: string = response['content']
              if(room){
                room.say(text)
              }else{
                contact?.say(text)
              }
            }else{
              //什么也不做呗
            }     
          }
      })
    }catch(e){
      console.log(e)
    }

    //待写：修改群名
  })
bot.start()
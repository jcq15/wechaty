# wechaty
本项目使用[wechaty-puppet-padplus](https://github.com/wechaty/wechaty-puppet-padplus)。请先查看[官方文档](https://github.com/wechaty/wechaty-puppet-padplus)。
[![Powered by Wechaty](https://img.shields.io/badge/Powered%20By-Wechaty-green.svg)](https://github.com/chatie/wechaty)
[![Wechaty开源激励计划](https://img.shields.io/badge/Wechaty-开源激励计划-green.svg)](https://github.com/juzibot/Welcome/wiki/Everything-about-Wechaty)

## Token 申请

我们可以参与[开源激励计划](https://github.com/juzibot/Welcome/wiki/Everything-about-Wechaty)获得一年免费 Token，也可以直接购买，200元/月。

## 快速开始

按照官方文档配置好后，替换 `bot.ts` 并将 `backend.py` 和 `baoshi.py` 放到目录内。

新建 `password.ts`:
```shell
vim password.ts
```
输入 `export const my_token = '你的token';` 即可设置 Token。

运行后端程序
```shell
python backend.py
```

运行前端程序
```shell
ts-node bot.ts
```

## 程序结构说明

- `bot.ts` 与微信直接对接，微信收到的消息会在这里初步处理并 post 给后端
- `backend.py` 根据消息来源所在的群聊分散到不同的模块处理
- `baoshi.py` 处理报时群

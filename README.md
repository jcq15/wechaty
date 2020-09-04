# wechaty
本项目使用[wechaty-puppet-padplus](https://github.com/wechaty/wechaty-puppet-padplus)。请先查看[官方文档](https://github.com/wechaty/wechaty-puppet-padplus)。

## Token 申请

Wechaty 需要 Token， 付费的 200 一个月，显然是买不起的，但我们可以参与[开源激励计划](https://github.com/juzibot/Welcome/wiki/Everything-about-Wechaty)获得一年免费 Token。

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
- `zijing.py` 该部分涉及隐私，未上传，`backend.py` 中的相关代码可以自行删除

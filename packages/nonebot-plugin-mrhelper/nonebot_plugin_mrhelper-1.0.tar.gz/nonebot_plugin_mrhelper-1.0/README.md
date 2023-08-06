<p align="center">
  <a href="https://v2.nonebot.dev/"><img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>
</p>

<div align="center">

# nonebot_plugin_mrhelper
_✨ NoneBot movie-robot小助手 插件 ✨_
</div>

<p align="center">
  <a href="https://raw.githubusercontent.com/cscs181/QQ-Github-Bot/master/LICENSE">
    <img src="https://img.shields.io/github/license/cscs181/QQ-Github-Bot.svg" alt="license">
  </a>
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">
</p>


## 插件介绍

-----

一个为movie-robot开发的qq机器人插件  \
之所以想要开发这个插件是因为群友们天天在群里让我帮他们订阅影片太特么烦了，而我自己又是个穷b，不肯买服务器搞内网穿透  \
群友可以自行注册账号、登录账号、订阅影片、查询影片信息等  \
一天极速开发 还是第一次用nonebot 代码能跑就行 可读性为0 ~~两天后我不确定我能否看懂自己的代码~~

## 环境配置

-----

### movie-robot地址 **必填** **（理论来说只需要配置这个就能成功跑起来了）**
`MRHELPER_MRURL="http://192.168.5.208:1329" #需包含协议头 端口 结尾不要有"/"`
### mrhelper的数据库位置 选填
`MRHELPER_DB="" #目录最后务必以mrhelper.db结尾 没填或填错默认为当前目录`
### 用于推送一些通知的qq号 选填
`MRHELPER_ADMIN=123456  #用于推送通知类消息 只能设置一个 不填会自动选取SUPERUSERS里的qq号`
### 是否启用emby注册功能（在注册mr账号时会同时自动注册一个同名emby账号） 选填
`MRHELPER_ENABLE_REGISTEREMBY=false #默认为关闭`
### emby地址 上边开启这个功能需要填
`MRHELPER_EMBYURL="http://192.168.5.208:8880" #需包含协议头 端口 结尾不要有"/"`
### emby apikey 上边开启这个功能需要填
`MRHELPER_EMBYAPIKEY="" #在emby后台获取的api密钥`
### 是否开启未读消息通知 选填
`MRHELPER_ENABLE_PUSHNOTIFY=true #会向上方设置的qq号推送mr的通知消息 默认开启`
### 是否开启自动通过好友请求 选填
`MRHELPER_AUTOADDFRIEND=true #默认开启(关闭后也会在收到好友请求时向上方qq号发消息 只是不会自动通过)`
## 命令一览

-----

‼注意：如果你发指令机器人不回复你 大概率是你忘记先登录了
1. #登录[空格]账号[空格]密码 用途：登录movie robot
2. #搜片[空格]片名 用途：等同于在网页手动搜索
3. #订阅[空格]数字 用途：搜片后用该命令选择相应序号
4. #站点数据 用途：查看当日上传下载等数据
5. #注册[空格]账号[空格]密码 用途：注册mr账号（可在配置文件中开启“同时注册emby账号”）
6. #搜库[空格]影片名/imdb_id 用途：查询影片是否入库等相关信息 建议使用imdb_id查询
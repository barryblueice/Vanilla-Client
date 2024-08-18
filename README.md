![Vanilla-Client](https://github.com/user-attachments/assets/e2253646-6f19-4dda-bae5-aefb635f21f6)

<p align="center">
    <a href="https://onebot.dev/"><img src="https://img.shields.io/badge/OneBot-12-black?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHAAAABwCAMAAADxPgR5AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAAxQTFRF////29vbr6+vAAAAk1hCcwAAAAR0Uk5T////AEAqqfQAAAKcSURBVHja7NrbctswDATQXfD//zlpO7FlmwAWIOnOtNaTM5JwDMa8E+PNFz7g3waJ24fviyDPgfhz8fHP39cBcBL9KoJbQUxjA2iYqHL3FAnvzhL4GtVNUcoSZe6eSHizBcK5LL7dBr2AUZlev1ARRHCljzRALIEog6H3U6bCIyqIZdAT0eBuJYaGiJaHSjmkYIZd+qSGWAQnIaz2OArVnX6vrItQvbhZJtVGB5qX9wKqCMkb9W7aexfCO/rwQRBzsDIsYx4AOz0nhAtWu7bqkEQBO0Pr+Ftjt5fFCUEbm0Sbgdu8WSgJ5NgH2iu46R/o1UcBXJsFusWF/QUaz3RwJMEgngfaGGdSxJkE/Yg4lOBryBiMwvAhZrVMUUvwqU7F05b5WLaUIN4M4hRocQQRnEedgsn7TZB3UCpRrIJwQfqvGwsg18EnI2uSVNC8t+0QmMXogvbPg/xk+Mnw/6kW/rraUlvqgmFreAA09xW5t0AFlHrQZ3CsgvZm0FbHNKyBmheBKIF2cCA8A600aHPmFtRB1XvMsJAiza7LpPog0UJwccKdzw8rdf8MyN2ePYF896LC5hTzdZqxb6VNXInaupARLDNBWgI8spq4T0Qb5H4vWfPmHo8OyB1ito+AysNNz0oglj1U955sjUN9d41LnrX2D/u7eRwxyOaOpfyevCWbTgDEoilsOnu7zsKhjRCsnD/QzhdkYLBLXjiK4f3UWmcx2M7PO21CKVTH84638NTplt6JIQH0ZwCNuiWAfvuLhdrcOYPVO9eW3A67l7hZtgaY9GZo9AFc6cryjoeFBIWeU+npnk/nLE0OxCHL1eQsc1IciehjpJv5mqCsjeopaH6r15/MrxNnVhu7tmcslay2gO2Z1QfcfX0JMACG41/u0RrI9QAAAABJRU5ErkJggg==" alt="onebot12"></a>
    <a href="https://github.com/barryblueice/Vanilla-Client/blob/main/LICENSE"><img src="https://img.shields.io/github/license/barryblueice/Vanilla-Client" alt="License"></a>
</p>

## 简介

[wxhelper](https://github.com/ttttupup/wxhelper)的OneBot V12客户端实现。

## 上游依赖

[wxhelper](https://github.com/ttttupup/wxhelper)：Hook WeChat / 微信逆向。

部分扩展API参考自[ComWeChatBotClient](https://github.com/JustUndertaker/ComWeChatBotClient)。

## 许可证

`Vanilla Client` 采用 [AGPLv3](https://github.com/barryblueice/Vanilla-Client/blob/main/LICENS) 协议开源，不鼓励、不支持一切商业使用。

## 关于支持：

Vanilla Client目前支持的微信版本为`3.9.8.25`，[可点击此处下载](https://github.com/tom-snow/wechat-windows-versions/releases/download/v3.9.8.25/WeChatSetup-3.9.8.25.exe)。

由于Vanilla Client的上游依赖[wxhelper](https://github.com/ttttupup/wxhelper)通过逆向微信得到的接口，故Vanilla Client仅支持`Windows`平台。

由于Vanilla Client的部分语法问题，故Vanilla Client仅支持`Python 3.1x`版本。

## Troubleshooting

如果你在使用过程中发现了bug，或者有好的想法，请速速提交[issue](https://github.com/barryblueice/Vanilla-Client/issues)，开发者会在第一时间进行处理。

也可进入[QQ交流群](https://qm.qq.com/q/t3jI6juvoQ)提交issue/获取最新进展。

<p align="center">
    <img src=https://github.com/user-attachments/assets/e6190d3d-9f2e-43a1-8641-d7462ce53304 width=400 /></img>
</p>

## 如何运行：

由于使用了poetry进行虚拟环境管理，故使用以下命令运行：

```python
poetry install
# poetry install --no-root

poetry run python main.py
```

## Onebot V12连接支持情况：

- [ ] HTTP
- [ ] HTTP Webhook
- [ ] 正向 Websocket
- [x] 反向 Websocket

## OneBot V12 Event实现情况：

**元事件：**
|Event|实现情况|备注
|:-:|:-:|:-:|
|meta.connect|✔️||
|meta.heartbeat|⭕|后续可能更新|
|meta.status_update|✔️||

**Message事件：**
|Event|实现情况|备注
|:-:|:-:|:-:|
|message.private|✔️|某些latest message事件可能会误触发</br>目前仅支持接收文本和部分notice事件|
|message.group|✔️|由于上游端限制，被at会通过文本检测，准确性可能存在误差</br>目前仅支持接收文本和部分notice事件|
|message.channel|❌|已知微信并没有类似两级群组的结构，故目前不考虑支持|

**Notice事件：**
|Event|实现情况|备注|
|:-:|:-:|:-:|
|notice.friend_increase|⭕|后续可能更新|
|notice.friend_decrease|⭕|后续可能更新|
|notice.private_message_delete|✔️||
|notice.group_member_increase|⭕|后续可能更新|
|notice.group_member_decrease|⭕|后续可能更新|
|notice.group_message_delete|✔️||
|notice.guild_member_increase|❌|已知微信并没有类似两级群组的结构，故目前不考虑支持|
|notice.guild_member_decrease|❌|已知微信并没有类似两级群组的结构，故目前不考虑支持|
|notice.channel_member_increase|❌|已知微信并没有类似两级群组的结构，故目前不考虑支持|
|notice.channel_member_decrease|❌|已知微信并没有类似两级群组的结构，故目前不考虑支持|
|notice.channel_message_delete|❌|已知微信并没有类似两级群组的结构，故目前不考虑支持|
|notice.channel_create|❌|已知微信并没有类似两级群组的结构，故目前不考虑支持|
|notice.channel_delete|❌|已知微信并没有类似两级群组的结构，故目前不考虑支持|

## OneBot V12 Action实现情况：

**用户Action：**
|Action|实现情况|备注|
|:-:|:-:|:-:|
|get_self_info|✔️||
|get_user_info|✔️|由于上游端限制，bot在群聊中会通过监听消息的方式收集群成员的wxid和username并保存为member.db。</br>在私聊事件中，若被触发wxid不存在于member.db，则username默认返回wxid。</br>你可以通过修改db文件的方式进行username的自定义。</br>通过数据库解包方式进行用户Action的实现暂不考虑支持。|
|get_friend_list|⭕|后续可能更新|

**Message Action:**
|Action|实现情况|备注|
|:-:|:-:|:-:|
|send_message|✔️/⭕|群聊/个人消息均支持。</br>目前仅支持发送图片和文本，文件发送仍在测试阶段，表情发送后续会支持。|
|delete_message|❌|因上游端问题无法实现|

**文件Action：**
|Action|实现情况|备注|
|:-:|:-:|:-:|
|upload_file|✔️||
|upload_file_fragmented|⭕|后续可能更新|
|get_file|⭕|忘记有没有写了|
|get_file_fragmented|⭕|后续可能更新|

**群组Action：**
|Action|实现情况|备注|
|:-:|:-:|:-:|
|get_group_info|⭕|后续可能更新|
|get_group_list|⭕|后续可能更新|
|get_group_member_info|⭕|后续可能更新|
|get_group_member_list|⭕|后续可能更新|
|set_group_name|⭕|后续可能更新|
|leave_group|⭕|后续可能更新|
|get_guild_info|❌|已知微信并没有类似两级群组的结构，故目前不考虑支持|
|get_guild_list|❌|已知微信并没有类似两级群组的结构，故目前不考虑支持|
|set_guild_name|❌|已知微信并没有类似两级群组的结构，故目前不考虑支持|
|get_guild_member_info|❌|已知微信并没有类似两级群组的结构，故目前不考虑支持|
|get_guild_member_list|❌|已知微信并没有类似两级群组的结构，故目前不考虑支持|
|leave_guild|❌|已知微信并没有类似两级群组的结构，故目前不考虑支持|
|get_channel_info|❌|已知微信并没有类似两级群组的结构，故目前不考虑支持|
|get_channel_list|❌|已知微信并没有类似两级群组的结构，故目前不考虑支持|
|set_channel_name|❌|已知微信并没有类似两级群组的结构，故目前不考虑支持|
|get_channel_member_info|❌|已知微信并没有类似两级群组的结构，故目前不考虑支持|
|get_channel_member_list|❌|已知微信并没有类似两级群组的结构，故目前不考虑支持|
|leave_channel|❌|已知微信并没有类似两级群组的结构，故目前不考虑支持|

**扩展Event：**

|Event|实现情况|备注|
|:-:|:-:|:-:|
|notice.get_private_poke|✔️|参考自[ComWeChatBotClient](https://justundertaker.github.io/ComWeChatBotClient/event/notice.html)，用法相同。|
|notice.wx.get_group_poke|✔️|参考自[ComWeChatBotClient](https://justundertaker.github.io/ComWeChatBotClient/event/notice.html)，用法相同。|

## 其他实现情况

|名称|实现情况|备注|
|:-:|:-:|:-:|
|OneBot V11支持|❌|由于wxid的性质与OneBot V11标准冲突，</br>（在OneBot V11中，user_id要求为int64），故不提供支持。|
|多开支持|❌|由于某些特殊原因，不提供支持。|

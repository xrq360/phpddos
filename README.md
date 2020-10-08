### 说明
一个基于php webshell的ddos攻击程序，包含控制端和客户端，支持tcp、udp、cc攻击方式。

ps：三年前写的，经过测试还能用。

### 文件解释
Control.py：python写的控制端程序，可批量管理shell，显示攻击结果，具体见Result.png

Target.txt：控制端的配置文件，内容是要攻击的目标网站。

Clents.txt：控制端使用，里面是webshell的具体网站，可根据具体情况进行更改。

Client.php和Client_bs64.php：ddos客户端程序，支持tcp、udp、cc攻击方式。Client.php是明文版本，Client_bs64.php是base64加密后的程序，利于隐藏。


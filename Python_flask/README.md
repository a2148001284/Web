# Python-Flask网站模板学习 #

**1.这里主要介绍了flask框架中常用的一些功能和模块**

**2.在这个框架中可以实现如下功能**

    /login 登陆界面
    /  主界面
    /login_address   处理POST包传送的登录信息
    /login_result    显示登录结果 会结合cookie和session保存信息
    /login_out   退出用户的登录
    /search  搜索用户名信息 通过GET 参数名uname进行传送
    /insert1   新用户的注册 或者叫插入新用户
    /insert   插入用户的数据库交互处理的后端页面
    /update   修改用户的密码 这里提供了三种方法验证用户的身份  避免越权
    /update_address  后端修改用户名和密码的验证逻辑3

框架模板会不断完善

后续会更新相应的Mysql数据库防火墙防注入功能模块！

后续还会借助python的flask框架搭建相应的web漏洞平台进行漏洞的学习！

## 使用切记 ##

**需要自行搭建mysql的环境保持开放才能运行相应的flask框架**

**同时需要建立相应的库 具体的修改方式已经通过图片的形式呈现**
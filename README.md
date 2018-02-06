# flask_movieweb
最近在跟着慕课网的flask项目课学习,  以前自己学过flask但是对网站的架构,业务逻辑都不太懂.正好借这次机会补补课

这个项目会记录项目不断搭建的过程

立个小flag: 尽快以笔记的形式总结出来发布到博客里面


下面是一些更新概要：

1. 第一版主要内容是使用sqlalchemy构造了数据库模型，使用jinja2构建前台和后台管理的页面并将页面路由搭建好。
1. 第二版将models文件的前半段的构造部分集成进了app的构造文件中。
1. 第三版关于管理员登陆功能，后台访问控制的实现和wtforms的使用
    1. 使用flask_wtf创建管理员登陆表单，将HTML文件中相关模块替换成jinja2语句，flask_wtf自动创建表单和按钮；
    1. 使用csrf进行表单保护
    1. 在models定义密码检查函数，使用werkzeug.security的check_password_hash函数
    1. 完整实现管理员登陆验证路由，查询数据库对比密码，若错误则flash错误信息并重定向到login页面，若正确则保存会话进入index
    1. **实现访问控制**(未登录情况下不能进入管理界面)

1. 第四版关注电影标签管理功能
    1. wtforms构建Tagform，使用jinja2更新HTML
    1. tag_add路由功能实现，数据对比，数据入库
    1. tag_add消息闪现功能
    1. tag_list路由功能实现
    1. **分页处理** 这里是[相关函数文档](http://www.pythondoc.com/flask-sqlalchemy/api.html)
    1. tag_del标签删除实现
    1. 最后实现了tag_edit功能

1. 第五版关注电影管理功能
    1. 使用wtforms创建文本框，文件传输框，下拉框，日期选择框等相关组件
    1. 表单内容存储操作
    1. **文件上传**
    1. 电影管理(删除,编辑)功能
    1. 编辑功能稍微复杂
## 这是我写的一个小玩意 可以帮助需要调剂的同学获得最新的消息
*因为只用了4个小时来写，估计会有很多bug，建议提issue 看到后会改，欢迎star && fork*

[教学视频(B站)](https://www.bilibili.com/video/BV1NZ4y1c7p7/)

B站审核已经通过，请大家尽量在b站观看，获得更好的观看体验！

[教学视频](https://pan.deniffer.com/teach.mp4)
### Usage:
* 使用须知
    * 你只需要一点点的配置就可以使用该文件
    * 第三方库依赖,如果缺少第三方库依赖，请自行Google下载安装如(pip install selenium) 建议使用anaconda 下述都是anaconda自带的
        * pandas
        * requests
        * selenium
        * schedule   //注意这个不是自带的 用于定时任务
    * 运行selenium 所需要的driver下载,以chromedriver为例 
    * 务必下载与chrome版本一致的driver，如何查看chrome版本，请自行Google
    * 关于selenium '--headless' 只是为了节省时间，并不利用debug

    * 关于程序正常运行时间， 慢是因为sleep操作(主要)导致的，

* 配置须知
    * 需提供chrome driver所在的路径，或者是当前工作目录
    * 提供属于你自己的研招网账号和密码，或者任一账号密码，因为只有登陆过后才可以访问调剂页面
    * 由于个人关系没有时间进行error control，欢迎有时间的人可以进行添加
    * 上一条的意思是你一旦输入某些错误信息，程序就会崩溃或者无法得到预期的结果
    * 如果使用其他邮箱作为sender，需要修改host_server, 如果使用gmail作为sender的话，请确保你本地环境的smtp协议走的是国外的流量，也就是意味着你需要一个可以代理TCP流量的东西，只代理http无法得到预期结果

    * 想到再补充

* 关于
    * 为什么不打包成二进制文件形式方便别人使用，原因有二：
        1. 由于运行代码需要个人信息(研招网)，为了避免被恶意使用所以给使用者带来适当的门槛我觉得是必需的
        2. 懒
    * 为什么不写一个图形用户界面，利用同上
    * 我希望使用者清楚明白的知道自己在干什么，包括代码的注释部分我也写得很清楚了
    * 为什么不将配置参数独立出来一个configuration而是直接修改源码，很简单，我希望你明白你自己在做什么
    * 为什么不模块化，主要是不想重构hhhh


### 工作原理 （可不看部分）
check.py 
* 通过selenium自动测试模块，模拟人的登录点击活动
    * 模拟点击页面并输入信息
    * 模拟翻页动作并采集数据
    * dafaframe.read_html() 读取每一页的表格信息
    * 合并每一页的dataframe
    * code的每一个sleep动作都是为了缓解指令执行的太快而导致的错误（如无法读取切换后的页面元素）
    * 将采集到的数据写入csv文件
    * 如果当前目录存在csv文件 ，则根据条件判断是否存在更新数据
    * 如果存在更新数据或者是第一次采集数据则发送邮件

scheduler.py
* 定时任务
    * 通过schedule模块定期执行job (设置的是每30分钟更新一次)
    * job是调用check.py文件

set_up_email.py
* 邮箱部分
    * 设置smtp的host
    * 设置发送邮件的形式(html)
    * 设置html的格式

**欢迎 pull request 和issue**
# -*- coding: UTF-8 -*-
__author__ = 'Chengrongkai'

# 浏览器驱动地址
driver_path = 'C://Users/Administrator/AppData/Local/Google/Chrome/Application/chromedriver.exe'
# 百家号登录名
baijihao_app_id = '1653603587770646'
# 百家号密码
baijihao_app_token = 'a40ac541731a832b42ac6410afbe716e'

# 趣头条
# 账号
qutoutiao_zhanghao = 15623826795
# 密码
qutoutiao_pwd = 'kai941021'


# 数据库连接信息
# 服务器ip地址
host='127.0.0.1'
# 端口号
port=3306
# 用户名
user='chengrongkai'
# 密码
passwd='kai941021'
# 数据库名
db='web_crawler'
# 字符集
charset='utf8mb4'
# 需要采集的网站:1、博客园;2、东方财富网;3、开源中国；4、csdn;5、掘金社区;6、大众娱乐;7、微信公众号;8、同花顺财经
config_spiders = [8]
# 发布的平台:1、百家号
config_publishers = [1]
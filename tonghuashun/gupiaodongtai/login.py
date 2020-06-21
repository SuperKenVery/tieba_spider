import js2py
import requests

# before_url = 'http://upass.10jqka.com.cn/login?redir=HTTP_REFERER'
# headers = {
#     'Cookie': 'searchGuide=sg; spversion=20130314; PHPSESSID=k954519g76gqn5rsskhg8r2qcutok6et; __utma=86410076.1322877608.1577776072.1577776072.1577776072.1; __utmc=86410076; __utmz=86410076.1577776072.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1577332464,1577343188,1577776045,1577779847; ths_login_uname=kai941021; log=; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1577948345; v=AgVUjwwK94nhxdPV49nBoLNXFEo8wrlUA3adqAdqwTxLniu8zxLJJJPGrXSU',
#     'Host': 'upass.10jqka.com.cn',
#     'Origin': 'http://upass.10jqka.com.cn',
#     'Referer': 'http://upass.10jqka.com.cn/',
#     'Upgrade-Insecure-Requests': '1',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
# }
# req = requests.get(url=before_url,headers=headers)
# print(req.cookies)


url = 'http://upass.10jqka.com.cn/login'

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie':'PHPSESSID=3tohjv93648s2cre97i7j0rmbna7krke; __guid=86410076.3396258109423624700.1577949865410.7236; monitor_count=1; v=AaujxdbuEZ_c8U1LtzS4le-PWmSvYN8FWXejlj3cpTVhvOUYxTBvMmlEM-VO',
    'Host': 'upass.10jqka.com.cn',
    'Origin': 'http://upass.10jqka.com.cn',
    'Referer': 'http://upass.10jqka.com.cn/login?redir=HTTP_REFERER',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}

uname = 'kai941021'
passwd = 'kai941021'

# js_url = 'http://s.thsi.cn/js/encrypt.min.js?t=201809011552'
# req = requests.get(url=js_url)
# js_req = req.text
context = js2py.EvalJs()
context.info = {'uname': uname,"passwd":passwd}
with open("encrypt.js", 'r', encoding='utf8') as f:
    context.execute(f.read())
    # - 执行加密密码的js字符
js = '''
        uname = thsencrypt.encode(info.uname);
        passwd = thsencrypt.encode(info.passwd);
      '''
context.execute(js)
# uname = context.s
print(context.uname)
print(context.passwd)
params = {
    'act': 'login_submit',
    'redir': 'http://www.10jqka.com.cn',
    'uname': context.uname,
    'passwd': context.passwd,
    'captchaCode':'',
    'longLogin': 'on',
    'rsa_version':'default_4',
    'submit': '登　录'
}

responseRes = requests.post(url, data = params, headers = headers)
# 无论是否登录成功，状态码一般都是 statusCode = 200
print(f"statusCode = {responseRes.status_code}")
print(f"text = {responseRes.text}")

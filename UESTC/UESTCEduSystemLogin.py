# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

# 初始化必备参数
url = 'http://idas.uestc.edu.cn/authserver/login?service=http%3A%2F%2Feams.uestc.edu.cn%2Feams%2Fhome.action'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

# 建立Session
s = requests.Session()
response = s.get(url, headers=headers)

# 获取登陆必备参数
soup = BeautifulSoup(response.text, 'lxml')
lt = soup.find('input', attrs={'name': 'lt'})['value']
execution = soup.find('input', attrs={'name': 'execution'})['value']


# 填写登陆信息
username = input('请输入用户名：')
password = input('请输入密码：')

# 创建表单
Form_Data = {
        'username': username,
        'password': password,
        'lt': lt,
        'dllt': 'userNamePasswordLogin',
        'execution': execution,
        '_eventId': 'submit',
        'rmShown': '1'
}

# 连续访问重定向页面
response = s.post(url=url, data=Form_Data, headers=headers, allow_redirects=False)
url = response.headers['Location']
response = s.get(url=url, headers=headers, allow_redirects=False)
url = response.headers['Location']
response = s.get(url=url, headers=headers)

# 验证登陆是否成功
response = s.get(url='http://eams.uestc.edu.cn/eams/home.action', headers=headers)
soup = BeautifulSoup(response.text, 'lxml')
try:
    name = soup.find('a', attrs={'href': '/eams/security/my.action'}).text + '，登陆成功！'
except:
    name = '登录失败 '
print(name)
import requests
from bs4 import BeautifulSoup
from PIL import Image

#初始化必备参数
url = 'http://202.202.83.66/default2.aspx'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

#建立Session
s = requests.Session()
response = s.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'lxml')
#print(soup.prettify())

#寻找Form的验证参数
__VIEWSTATE = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']

#获取登陆用验证码
CheckCode = 'http://202.202.83.66/CheckCode.aspx'
pic = s.get(CheckCode, headers=headers)
with open(r'ver_pic.png','wb') as f:
    f.write(pic.content)

#填写登陆信息
username = input("输入用户名: ")
password = input("输入密码 ")
 
#打开验证码图片
image = Image.open('ver_pic.png')
image.show()
ycode = input("输入弹出的验证码: ")

#建立Form Data
Form_Data = {
    '__VIEWSTATE': __VIEWSTATE,
    'txtUserName': username,
    'TextBox2': password,
    'txtSecretCode': ycode,
    'RadioButtonList1': '%D1%A7%C9%FA', #学生GB2312格式
    'Button1': '',
    'lbLanguage': '',
    'hidPdrs': '',
    'hidsc': '',
}

#模拟登陆
response = s.post(url, data=Form_Data, headers=headers)
#response = s.get(url='http://202.202.83.66/xs_main.aspx?xh=' + username, headers=headers, cookies=s.cookies)
soup = BeautifulSoup(response.text, 'lxml')
try:
    name = soup.find('span', attrs={'id': 'xhxm'}).text + '，登陆成功！'
except:
    name = '登录失败 '
print(name)
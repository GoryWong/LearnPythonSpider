# -*- coding: utf-8 -*-

# @Author: 王国瑞
# @File: UESTCexams.py                                                                 
# @Time: 2018/7/24                                   
# @Contact: frantik@qq.com
# @Description: 模拟登陆教务系统获取并下载历年成绩

import requests
from bs4 import BeautifulSoup
import csv

def Login(url, headers):
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

    return s



def GetScores(s, headers):
    response = s.get('http://eams.uestc.edu.cn/eams/teach/grade/course/person!historyCourseGrade.action?projectType=MAJOR', headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    Score_table = soup.find('table', attrs={'id': 'grid21344342991'})
    Score_tbody = soup.find('tbody', attrs={'id': 'grid21344342991_data'})
    Score_head = Score_table.find_all('th')
    head = []
    for th in Score_head:
        head.append(th.string)
    Score_lists = Score_tbody.find_all('tr')

    with open('results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(head)
        for tr in Score_lists:
            lst = []
            Score_list = tr.find_all('td')
            for td in Score_list:
                try:
                    lst.append(td.string.strip())
                except:
                    lst.append('无')
            writer.writerow(lst)

            
def main():
    #初始化必备参数
    url = 'http://idas.uestc.edu.cn/authserver/login?service=http%3A%2F%2Feams.uestc.edu.cn%2Feams%2Fhome.action'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    s = Login(url, headers)
    GetScores(s, headers)
    print('成绩已下载，保存在 results.csv.')
    input('Press any key...')

if __name__ == '__main__':
    main()
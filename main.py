#爬虫模块
import requests  
from bs4 import BeautifulSoup 
#发邮件模块
import smtplib
from email.mime.text import MIMEText
from email.header import Header
#定义发邮件函数
def Sendmessage(msg, From_content, To_content, subject, Form,sender, receivers, password):
    message = MIMEText(msg, 'html', Form)
    message['From'] = Header(From_content, Form)
    message['To'] = Header(To_content, Form)
    message['Subject'] = Header(subject, Form)
    smtp = smtplib.SMTP_SSL('smtp.qq.com', 465)
    smtp.login(sender, password)
    smtp.sendmail(sender, receivers, message.as_string())
    smtp.quit()
#设置发件人，password为邮箱授权码，eceives为收件人列表，设置编码格式，编辑邮件内容和标题
sender = 'xxxxxx@qq.com'
password = 'xxxxxxxx'
receivers = ['xxxxxxx@qq.com']      #不建议设置过多收件人，会引发QQ频率检测
From_content = 'Aether-supper-bot'
To_content = ' '
subject = '西北大学教务处通知监听机器人'
Form = 'utf-8'

#请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53',
    'Host':'jwc.nwu.edu.cn',
    }
#发送url请求
url = 'https://jwc.nwu.edu.cn/'
response = requests.get(url, headers=headers)  
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text,'lxml')

#保存日志
def Save_summary(tips):
    f = open('教务处通知日志.txt','a',encoding='UTF-8')
    f.write(tips)
    f.close()
    
#最新消息
news = soup.body.find_all(class_ = "main2-list fl")[0]
sort = news.find_all(class_ = "main2-l")[0].string
massage = news.find_all(target="_blank")[1].string
when = news.find_all(class_ = "main2-d")[0].string
web =url + news.find_all(name = 'a')[1].attrs['href']
tips = '学校教务处最新通知：\n时间：' + when +'\n类别：' + sort + '类\n通知概要：'+ massage + '\n原文链接：' + web + "\n" + '-'*50 + '\n'
print(tips)

#主体代码（将循环运行以监听）
try:        #非首次运行则判断新消息与上次日志消息是否相同
    fi = open('教务处最新通知.txt','r',encoding='UTF-8')
    line = fi.readlines()[3].split("：")[1].replace('\n','')
    print(line)
    if massage == line:         #相同就不发邮件
        print('无最新消息')
    else:                       #不同则发送邮件
        print('有最新消息')
        Sendmessage(tips, From_content, To_content, subject, Form,sender,receivers,password)
        print('已发送最新通知')
        fi.close()
        fi = open('教务处最新通知.txt','w',encoding='UTF-8')
        fi.write(tips)
        Save_summary(tips)
        print('已更新日志')
except:        #首次运行新建日志
    fi = open('教务处最新通知.txt','w+',encoding='UTF-8')
    fi.write(tips)
    Save_summary(tips)
    print('已新创建日志')
    Sendmessage(tips, From_content, To_content, subject, Form , sender , receivers, password)
    print('已发送最新通知')
fi.close()

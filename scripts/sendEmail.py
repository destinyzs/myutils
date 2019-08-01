# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr



sender = 'xx' ## Sender
password = 'xx' 
## Send to myself
receiver = sender


def SendMail(_subject, _content, 
            _from = sender, _password = password, _to = receiver):

    try:
        msg = MIMEText(_text = _content, _subtype = 'plain', _charset = 'utf-8') ## content
        msg['From'] = formataddr(['From_' + _from.split('@')[0], _from]) ## nickname, sender
        msg['To'] = formataddr(['To_' + _to.split('@')[0], _to]) ## nickname, receiver
        msg['Subject'] = _subject ## subject

        server = smtplib.SMTP_SSL(host = 'smtp.qq.com', port = 465)
        server.login(user = _from, password = _password) ## Login
        server.sendmail(_from, [_to], msg = msg.as_string())
        server.quit()
        flag = True
    except Exception as e:
        print(e)
        flag = False
    
    re = 'Success!' if flag else 'Fail !!!'
    print(re)

if __name__ == '__main__':

    #############################################
    ##### Only support qq mail/foxmail Now.
    #############################################


    sender = 'xx' ## Sender
    password = 'xx' 
    ## Send to myself
    receiver = sender

    subject = 'Hi'
    content = 'Hello World!'


    SendMail(_from = sender, _password = password, _to = receiver, _subject = subject, _content = content)

#email送信モジュール
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib
from os.path import basename

def con(accnt, pwd, msg):
    #メール設定の情報
    smtp_host = 'smtp.gmail.com'# そのまま
    smtp_port = 587# そのまま
     # メールサーバーへアクセス
    server = smtplib.SMTP(smtp_host, smtp_port)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(accnt, pwd)
    server.send_message(msg)
    server.quit()

def crtMsg(_from, to, sub, mainMsg):
     # メールの内容を作成
     msg = MIMEMultipart()
     # 件名
     msg['Subject'] = sub
     # メール送信元 
     msg['From'] = _from 
     #メール送信先
     msg['To'] = to 

     # ファイルを添付
     msg.attach(MIMEText(mainMsg))
     return msg

def send(_from, pwd, sub, mainMsg):
     msg = crtMsg(_from, _from, sub, mainMsg)
     con(_from, pwd, msg)

def sendAttach(_from, pwd, sub, mainMsg, attachPath):
     msg = crtMsg(_from, _from, sub, mainMsg)
     # ファイルを添付
     with open(attachPath, "rb") as f:
         part = MIMEApplication(
             f.read(),
             Name=basename(attachPath)
         )
     part['Content-Disposition'] = 'attachment; filename="%s"' % basename(attachPath)
     msg.attach(part)
     con(_from, pwd, msg)


    

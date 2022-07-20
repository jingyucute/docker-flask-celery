#!user/bin/python
# _*_ coding: utf-8 _*_

from abc import ABCMeta, abstractclassmethod

from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr, parseaddr
import os

class BaseEmail(metaclass=ABCMeta):
    
    def __init__(self, host, port, user, pwd):
        '''
            对象初始化
            host: 邮件服务器地址
            port: 邮件服务器端口
            user: 配置的邮件用户
            pwd: 配置的密码
            smtp: SMTP实例化对象, 用来发送邮件
            message: 构建的邮件主体
            receivers: 将要发送的用户
                配置两种形式, 
                  list, ["xxx1@qq.com", "xxx2@qq.com"]
                  dict, {"to": ["xxx1@qq.com"], "cc": ["yyy1@qq.com"], "bcc": ["zzz1@qq.com"]}
        '''
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd
        self.smtp = None
        self.message = None
        self.receivers = None
    
    @abstractclassmethod
    def login(self, proxy_congigs=None):
        '''
            登陆邮箱服务器
            proxy_configs: 使用代理相关配置
                {
                    "type": 代理类型,  SOCKS4, SOCKS5, HTTP
                    "ip": "主机地址", 
                    "port": "端口号"
                }
        '''
        return "login email server"


    def _format_addr(self, s):
        ## 美化发送人
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def _get_attachment(self, file):
        '''
            根据文件路径， 封装附件
        '''
        path, filename = os.path.split(file)
        attach = MIMEApplication(open(file, 'rb').read())
        attach.add_header("Content-Disposition", "attachment", filename=Header(filename, "utf-8").encode())
        return attach


    def _get_attachment_part(self, attachments=[]):
        '''
            根据附件参数， 封装附件列表
        '''
        attachparts = []
        if isinstance(attachments, list):
            for file in attachments:
                attachparts.append(self._get_attachment(file))
        elif isinstance(attachments, dict):
            for k, files in attachments.items():
                for file in files:
                    attachparts.append(self._get_attachment(file))
        elif isinstance(attachments,str):
           attachparts.append(self._get_attachment(attachments))

        return attachparts

    
    def write_email(self, subject, content, receivers, attachments=[], email_type="plain", butify_name=""):
        '''
            封装邮件主体部分
            subject: 邮件主题
            content: 邮件正文
            receivers: 收件人列表, 初始化中的方法一致
            attachments: 邮件附件
                配置两种形式
                  list, ["/a/b/c/hhh.txt", "/a/e/f/ttt.pdf"]  默认是文件格式
                  dict, {"file": [], "image": []}
            email_type: 邮件类型， 是发送的文本邮件, 还是html邮件

            在正文中放入图片, 需要设置图片图片和引用信息
        '''

        try:
            self.receivers = receivers

            # 封装邮件主体
            message = MIMEMultipart("mixed")
            # 发送人配置
            message['From'] = self._format_addr("%s<%s>" % (butify_name, self.user)) if butify_name else self.user
            # 收件人配置
            if isinstance(receivers, list):
                message["To"] = ",".join(receivers)
            elif isinstance(receivers, dict):
                if 'to' not in receivers:
                    raise Exception("收件人dict参数不正确")
                message["To"] = ",".join(receivers['to']) if isinstance(receivers['to'], list) else receivers['to']
                if 'cc' in receivers:
                    message["Cc"] = ",".join(receivers['cc']) if isinstance(receivers['cc'], list) else receivers['cc']
                if "bcc" in receivers:
                    message["Bcc"] = ",".join(receivers['bcc']) if isinstance(receivers['bcc'], list) else receivers['bcc']
            elif isinstance(receivers, str):
                message["To"] = receivers
            else:
                raise Exception("收件人参数格式不正确")

            # 邮件主题
            message['Subject'] = Header(subject, "utf-8")

            # 邮件正文
            alternative = MIMEMultipart("alternative")
            if email_type == "html":
                alternative.attach(MIMEText(content, _subtype='html', _charset='UTF-8'))
            else:
                alternative.attach(MIMEText(content, _subtype='plain', _charset='UTF-8'))
            message.attach(alternative)
            # 附件部分
            files = []
            images = []
            if isinstance(attachments, list):
                for attachment in attachments:
                    file, ext = os.path.splitext(attachment)
                    if ext in [".bmp", ".dib", ".png", ".jpg", ".jpeg", ".pbm", ".pgm", ".ppm", ".tif", ".tiff"]:
                        images.append(attachment)
                    else:
                        files.append(attachment)
            elif isinstance(attachments, dict):
                if 'file' in attachments:
                    files = attachments['file']
                if 'image' in attachments:
                    images = attachments['image']
            ## 文件附件
            for file in files:
                message.attach(self._get_attachment(file))

             ## 图片附件
            for image in images:
                attach = self._get_attachment(image)
                ## 这里可以实现将图片放入html文本中， 需要引用id， 这个功能暂时不实现
                # attach.add_header("Content-ID", "<image1>")
                message.attach(attach)

            # attachparts = self._get_attachment_part(attachments)
            # for attach in attachparts:
            #     message.attach(attach)

            self.message = message
            print("-- smtp write email success --")
        except Exception as e:
            raise e

    def send_mail(self):
        try:
            receivers = []
            if isinstance(self.receivers, list):
                receivers = self.receivers
            elif isinstance(self.receivers, dict):
               pass
            elif isinstance(self.receivers, str):
                receivers = [self.receivers]
            self.smtp.sendmail(self.user, receivers, self.message.as_string())
            print("-- smtp send email success --")
        except Exception as e:
            raise e 
        return "send content"

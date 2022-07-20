#!user/bin/python
# _*_ coding: utf-8 _*_

from .BaseEmail import BaseEmail
import smtplib

class SimpleEmail(BaseEmail):
    
    def login(self, proxy_configs=None):
        
        try:
            if proxy_configs:
                import socks
                if proxy_configs['type'] == "SOCKS4":
                    socks.set_default_proxy(socks.PROXY_TYPE_SOCKS4, proxy_configs['ip'], proxy_configs["port"])
                elif proxy_configs['type'] == "SOCKS5":
                    socks.set_default_proxy(socks.PROXY_TYPE_SOCKS5, proxy_configs['ip'], proxy_configs["port"])
                else:
                    socks.set_default_proxy(socks.PROXY_TYPE_HTTP, proxy_configs['ip'], proxy_configs["port"])
                socks.wrap_module(smtplib)
            
            self.smtp = smtplib.SMTP()
            self.smtp.connect(self.host, self.port)
            self.smtp.starttls()
            self.smtp.ehlo() 
            self.smtp.login(self.user, self.pwd)
            print("-- smtp login success --")
        except Exception as e:
            raise e
        
#!user/bin/python
# _*_ coding: utf-8 _*_

from mail import BerryEmail

if __name__ == "__main__":
    # print(os.path.splitext("/a/b/c/t.txt"))
    # email = SimpleEmail(**{
    #     'host': "smtp.qq.com",
    #     "port": 465,
    #     "user": "1830065688@qq.com",
    #     "pwd": "pywulnzxffjbebbf"
    # })
    # email.login({"type": "SOCKS5", "ip": "127.0.0.1", "port": 7890})
    # email.write_email("测试邮件", "测试内容", ["jingyucute@gmail.com"], attachments=["./requirements.txt", "/Users/jingyu/jingyu.jpeg"] , butify_name="Jingyu")
    # email.send_mail()

    berry = BerryEmail(**{
        "host": "mail.berrygenomics.com",
        "port": 25,
        "user": "analyst_1@berrygenomics.com",
        "pwd": "DAS@.analyst06"
    })
    berry.login()
    berry.write_email("测试邮件", "测试内容", ["1830065688@qq.com"], attachments=["./requirements.txt", "/Users/jingyu/jingyu.jpeg", "/Users/jingyu/Navicat_Premium_16.0.13_macwk.com.dmg"] , butify_name="Jingyu")
    berry.send_mail()




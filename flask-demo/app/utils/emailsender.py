import smtplib
import email.mime.multipart
import email.mime.text
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import logging

logger = logging.getLogger(__name__)


class EmailSender:
    __address = ''
    __authcode = ''
    __stmphost = ''
    __stmpport = 465

    @classmethod
    def get_address(cls):
        return cls.__address

    @classmethod
    def set_address(cls, address):
        cls.__address = address

    @classmethod
    def get_authcode(cls):
        return cls.__authcode

    @classmethod
    def set_authcode(cls, password):
        cls.__authcode = password

    @classmethod
    def set_stmphost(cls, stmphost):
        cls.__stmphost = stmphost

    @classmethod
    def get_stmphost(cls):
        return cls.__stmphost

    @classmethod
    def set_stmpport(cls, stmpport):
        cls.__stmpport = stmpport

    @classmethod
    def get_stmpport(cls):
        return cls.__stmpport

    @staticmethod
    def send_email(receivers, user_name, user_email, attach, filename):
        """
        发送邮件
        :param receivers:邮箱地址，多个邮箱使用;进行分割
        :param user_name:用户名
        :param user_email:用户邮件地址
        :param attach:附件流
        :param filename:附件名
        :return:
        """
        try:
            msg = email.mime.multipart.MIMEMultipart()
            msg['from'] = EmailSender.get_address()
            msg['to'] = receivers  # 多个收件人的邮箱应该放在字符串中,用字符分隔, 然后用split()分开,不能放在列表中, 因为要使用encode属性
            msg['subject'] = '估值表'
            content = '用户' + user_name + '通过系统为您发送了估值表，请查收！'
            txt = email.mime.text.MIMEText(content, 'plain', 'utf-8')
            msg.attach(txt)
            # 添加附件，从本地路径读取。如果添加多个附件，可以定义part_2,part_3等，然后使用part_2.add_header()和msg.attach(part_2)即可。
            part = MIMEApplication(attach)
            part.add_header('Content-Disposition', 'attachment', filename=filename)  # 给附件重命名,一般和原文件名一样,改错了可能无法打开.
            msg.attach(part)
            smtp = smtplib.SMTP_SSL(EmailSender.get_stmphost(),
                                    EmailSender.get_stmpport())  # 需要一个安全的连接，用SSL的方式去登录得用SMTP_SSL，之前用的是SMTP（）.端口号465或587
            smtp.login(EmailSender.get_address(), EmailSender.get_authcode())  # 发送方的邮箱，和授权码（不是邮箱登录密码）
            smtp.sendmail(EmailSender.get_address(), receivers.split(";"),
                          str(msg))  # 注意, 这里的收件方可以是多个邮箱,用";"分开, 也可以用其他符号
            smtp.quit()
            return True
        except smtplib.SMTPException as e:
            logger.error(e)
            return False

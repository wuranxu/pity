import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import make_msgid

from awaits.awaitable import awaitable
from jinja2.environment import Template

from app.core.configuration import SystemConfiguration
from app.core.msg.notification import Notification
from config import Config


class Email(Notification):

    # @staticmethod
    # def get_mail_client():
    #     configuration = SystemConfiguration.get_config()
    #     data = configuration.get("email")
    #     return yagmail.SMTP(user=data.get("sender"), password=data.get("password"), host=data.get("host"))
    #
    # @staticmethod
    # def send_msg(subject, content, attachment=None, *receiver):
    #     client = Email.get_mail_client()
    #     client.send(receiver, subject=subject, contents=content, attachments=attachment)

    @staticmethod
    @awaitable
    def send_msg(subject, content, attachment=None, *receiver):
        configuration = SystemConfiguration.get_config()
        data = configuration.get("email")
        sender = data.get("sender")
        message = MIMEText(content, 'html', 'utf-8')
        message['From'] = sender
        # 抄送给自己一份
        message['Subject'] = Header(subject, 'utf-8')
        message['Message-ID'] = make_msgid()

        try:
            smtp = smtplib.SMTP()
            smtp.connect(data.get("host"))
            # 我们用set_debuglevel(1)就可以打印出和SMTP服务器交互的所有信息。
            smtp.set_debuglevel(1)
            smtp.login(sender, data.get("password"))
            smtp.sendmail(sender, [sender, *receiver], message.as_string())
        except Exception as e:
            raise Exception(f"发送测试报告邮件失败: {e}")

    @staticmethod
    def render_html(filepath=Config.REPORT_PATH, **kwargs):
        with open(filepath, encoding="utf-8") as f:
            html = Template(f.read())
            # 渲染html模板
            return html.render(**kwargs)

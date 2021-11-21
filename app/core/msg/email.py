import yagmail

from app.core.configuration import SystemConfiguration
from app.core.msg.notification import Notification


class Email(Notification):

    @staticmethod
    def get_mail_client():
        configuration = SystemConfiguration.get_config()
        data = configuration.get("email")
        return yagmail.SMTP(user=data.get("sender"), password=data.get("password"), host=data.get("host"))

    @staticmethod
    def send_msg(subject, content, attachment=None, *receiver):
        client = Email.get_mail_client()
        client.send(receiver, subject=subject, contents=content, attachments=attachment)

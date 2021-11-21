from abc import ABC


class Notification(ABC):

    @staticmethod
    def send_msg(subject, content, attachment=None, *receiver):
        pass

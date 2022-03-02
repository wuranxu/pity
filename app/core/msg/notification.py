class Notification(object):

    @staticmethod
    def send_msg(subject, content, attachment=None, *receiver):
        raise NotImplementedError

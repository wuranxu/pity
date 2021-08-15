from datetime import datetime


class CaseLog(object):

    def __init__(self):
        self.log = list()

    def append(self, content, end=True):
        if end:
            self.log.append("[{}]: 步骤结束 -> {}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), content))
        else:
            self.log.append("[{}]: 步骤开始 -> {}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), content))

    def o_append(self, content):
        """
        原始append
        :param content:
        :return:
        """
        self.log.append(content)

    def join(self):
        return "\n".join(self.log)

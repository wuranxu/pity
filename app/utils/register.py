import socket

import yaml
from yaml import FullLoader


class ServiceRegister(object):

    @staticmethod
    def parse_config(filepath):
        """
        解析服务配置，以便于注册进etcd
        :param filepath:
        :return:
        """
        with open(filepath, 'r', encoding='UTF-8') as f:
            data = yaml.load(f, FullLoader)
            return data

    @staticmethod
    def get_ip_address():
        """
        获取本机ip地址
        :return:
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]

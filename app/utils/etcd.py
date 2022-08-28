import json
import time

import etcd3


class EtcdClient(object):
    client = None
    scheme = "pity"

    def __init__(self, host, port, **kwargs):
        self.client = etcd3.client(host, port, **kwargs)

    def unregister_service(self, name, addr):
        self.client.delete("/{}/{}/{}".format(self.scheme, name, addr))

    def register_service(self, name, addr, ttl):
        while True:
            value, meta = self.client.get("/{}/{}/{}".format(self.scheme, name, addr))
            if value is None:
                self.with_alive(name, addr, ttl)
            time.sleep(ttl)

    @staticmethod
    def lower_first(s: str):
        if len(s) == 0:
            return ""
        if not s[0].islower():
            return s[0].lower() + s[1:]
        return s

    def register_api(self, name, instance, cfg):
        version = cfg.get("version")
        methods = cfg.get("method", {})
        for d in dir(instance):
            if d.startswith("_") or d.endswith("_"):
                continue
            if d not in methods.keys():
                print("方法: {}注册失败, 请在service.yml中配置".format(d))
                continue
            info = methods.get(d)
            self.register_single(version, name, d, info)

    def register_single(self, version, service, method_name, no_auth=None):
        key = "{}.{}.{}".format(version, EtcdClient.lower_first(service), EtcdClient.lower_first(method_name))
        info = {"authorization": False if no_auth is None else no_auth.get("authorization"),
                "path": "/{}/{}".format(service, method_name)}
        self.client.put(key, json.dumps(info, ensure_ascii=False))

    def with_alive(self, name, addr, ttl):
        lease = self.client.lease(ttl)
        key = "/{}/{}/{}".format(self.scheme, name, addr)
        print("service alive: {}".format(key))
        self.client.put(key, addr, lease=lease)
        self.refresh_lease(lease, ttl)

    def refresh_lease(self, lease, ttl):
        try:
            while True:
                next(self.client.refresh_lease(lease.id))
                print("续租了")
                time.sleep(ttl - 5)
        except Exception as err:
            print("续租失败, error: ", err)

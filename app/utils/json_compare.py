import json

from app.utils.decorator import SingletonDecorator


@SingletonDecorator
class JsonCompare(object):

    def compare(self, exp, act):
        ans = []
        self._compare(exp, act, ans, '$')
        return ans

    def _compare(self, a, b, ans, path):
        a = self._to_json(a)
        b = self._to_json(b)
        if type(a) != type(b):
            ans.append(f"{path} 类型不一致, 分别为{type(a)} {type(b)}【❌】")
            return
        if isinstance(a, dict):
            keys = []
            for key in a.keys():
                pt = path + "." + key
                if key in b.keys():
                    self._compare(a[key], b[key], ans, pt)
                    keys.append(key)
                else:
                    ans.append(f"{pt} 在实际结果中不存在【❌】")
            for key in b.keys():
                if key not in keys:
                    pt = path + "." + key
                    ans.append(f"{pt} 在实际结果中多出【❌】")
        elif isinstance(a, list):
            i = j = 0
            while i < len(a):
                pt = f"{path}[{i}]"
                if j >= len(b):
                    ans.append(f"{pt} 在实际结果中不存在【❌】")
                    i += 1
                    j += 1
                    continue
                self._compare(a[i], b[j], ans, pt)
                i += 1
                j += 1
            while j < len(b):
                pt = f"{path}[{j}]"
                ans.append(f"{pt} 在预期结果中不存在【❌】")
                j += 1
        else:
            if a != b:
                ans.append(
                    f"{path} 数据不一致: {a} 【❌】"
                    f"!= {b}" if path != "" else
                    f"数据不一致: {a} != {b}【❌】")

    def _to_json(self, string):
        try:
            float(string)
            return string
        except:
            try:
                if isinstance(string, str):
                    return json.loads(string)
                return string
            except:
                return string

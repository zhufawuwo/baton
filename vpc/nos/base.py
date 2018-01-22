#! python3
# coding: utf-8
from collections import namedtuple

class NetworkElement():
    def __init__(self,nid):
        self.nid = nid

class NetworkElementEvent(dict):
    def __init__(self,eid,nid,type):
        self["eid"] = eid
        self["nid"] = nid
        self["type"] = type

    @property
    def eid(self):
        return self.get("eid")

    @property
    def nid(self):
        return self.get("nid")

    @property
    def type(self):
        return self.get("type")

    @property
    def header(self):
        Header = namedtuple("Header",["eid","nid","type"])
        return Header(eid=self.eid,nid=self.nid,type=self.type)

    @property
    def body(self):
        ret = {}
        for (k,v) in self.items() :
            if k not in ("eid","nid","type") :
                ret[k] = v
        return ret


if __name__ == "__main__":
    pass
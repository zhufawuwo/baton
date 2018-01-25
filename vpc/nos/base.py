#! python3
# coding: utf-8
from collections import namedtuple
from enum import Enum

from pub import *
from pub.tree import Node
from pub.utils import singleton,EnumBase

class NetworkElement():
    def __init__(self):
        self._id = guid()

    @property
    def id(self):
        return self._id


class NetworkElementEvent(dict):
    def __init__(self,nid,type):
        self["id"] = guid()
        self["ne_id"] = nid
        self["type"] = type

    @property
    def id(self):
        return self.get("id")

    @property
    def ne_id(self):
        return self.get("ne_id")

    @property
    def type(self):
        return self.get("type")

    @property
    def header(self):
        Header = namedtuple("Header",["id","ne_id","type"])
        return Header(eid=self.id,nid=self.ne_id,type=self.type)

    @property
    def body(self):
        ret = {}
        for (k,v) in self.items() :
            if k not in ("id","ne_id","type") :
                ret[k] = v
        return ret

event_t = EnumBase(prefix='NE_',members=["ONLINE","OFFLINE"],type=EnumBase.BIT_SHIFT)


class EventNode(Node):
    ENTRANCE = 1
    FILTER = 2
    APP = 3

    def __init__(self,name,tag):
        super().__init__(name)
        self._tag = tag

    @property
    def tag(self):
        return self._tag

    def _dispatch(self,event):
        for child in self._children:
            child.dispatch(event)

    def handle_event(self,event):
        self._dispatch(event)

@singleton
class EventChain(EventNode):
    def __init__(self):
        super().__init__("entrance",EventNode.ENTRANCE)

    def feed(self,e):
        print(e)
        self.handle_event(e)

class EventFilter(EventNode):
    def __init__(self,name,f,**kargs):
        super().__init__(name)
        self.tag = EventNode.ENTRANCE
        self.filter = f
        self.kargs = kargs

    def handle_event(self,event):
        if self.f(event,**self.kargs) :
            self._dispatch(event)

def event_type_filter(event,type):
    return event.type & type


@singleton
class NetworkElementRegister():
    def __init__(self):
        self._nes = {}

    def register(self,ne):
        self._nes[ne.id] = ne

    def remove(self,ne_id):
        return self._nes.pop(ne_id)



if __name__ == "__main__":
    e = NetworkElementEvent(1,2,3)
    print(e.eid)
    print(e.header)
    e["data"] = b'0x11'
    print(e.body)

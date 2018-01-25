#! python3
# coding: utf-8
from vpc.nos import NetworkElement,NetworkElementEvent,event_t

class OVSEvent(NetworkElementEvent):

    def __init__(self,eid,nid,type):
        super().__init__(eid,nid,type)


class OVS(NetworkElement):
    def __init__(self,nid,channel):
        super().__init__(nid)
        self.chn = channel
        self.ofp = self.chn.ofp





if __name__ == "__main__":
    pass
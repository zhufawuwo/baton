#! python3
# coding: utf-8
from vpc.nos import NetworkElement,NetworkElementEvent,event_t,EventChain

class OVSEvent(NetworkElementEvent):

    def __init__(self,eid,nid,type):
        super().__init__(eid,nid,type)


class OVS(NetworkElement):
    def __init__(self,nid,channel,datapath):
        super().__init__(nid)
        self.chn = channel
        self.ofp = self.chn.ofp
        self._datapath = datapath

    @property
    def datapath(self):
        return self._datapath






if __name__ == "__main__":
    pass
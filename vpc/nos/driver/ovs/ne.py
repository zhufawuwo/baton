#! python3
# coding: utf-8
from vpc.nos import NetworkElement,NetworkElementEvent,event_t,EventChain

class OVSEvent(NetworkElementEvent):
    def __init__(self,ne_id,type):
        super().__init__(ne_id,type)


class OVS(NetworkElement):
    def __init__(self,channel,datapath):
        super().__init__()
        self.chn = channel
        self.ofp = self.chn.ofp
        self._datapath = datapath

    @property
    def datapath(self):
        return self._datapath


    def ne_online(self):
        e = OVSEvent(self.id,event_t.NE_ONLINE)
        EventChain.feed(e)





if __name__ == "__main__":
    pass
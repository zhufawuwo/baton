#! python3
# coding: utf-8
from vpc.nos import NetworkElement

class OVS(NetworkElement):
    def __init__(self,nid,channel):
        super().__init__(nid)
        self.chn = channel
        self.ofp = self.chn.ofp






if __name__ == "__main__":
    pass
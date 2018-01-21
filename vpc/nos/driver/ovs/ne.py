#! python3
# coding: utf-8
from vpc.nos import NetworkElement

class OVS(NetworkElement):
    def __init__(self,nid,channel):
        super().__init__(nid)
        self.chn = channel
        self.ofp = self.chn.ofp

    def handle_ofp_message(self,msg):
        version,oftype,len,xid = self.ofp.p.parse_ofp_header(msg)
        if oftype in self._msg_map :
            handler = self._msg_map[oftype]
            handler(msg)





if __name__ == "__main__":
    pass
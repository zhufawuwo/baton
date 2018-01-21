#! python3
# coding:utf-8
from twisted.internet import reactor
from twisted.internet.protocol import Protocol,Factory,connectionDone

from pub import *
from vpc.nos.driver.ovs.openflow import OpenFlowProtocol as OFP


class OpenFlowChannel(Protocol):
    def __init__(self):
        super().__init__()
        self.versions = set(map(float,str(conf.get("protocol","versions")).split('|')))
        self.ofp = None
        self._mmap = {}

    def _init_msg_map(self,ofp):
        for x in dir(ofp):
            if x.startswith("OFP"):
                print(x)
                msg_type = getattr(ofp,x)
                handler = getattr(self,"handle_"+x,None)
                if handler :
                    self._mmap[msg_type] = handler

        print(self._mmap)


    def _dispath_openflow_message(self, msg):
        ver, oftype, len, xid = OFP.parse_ofp_header(msg)
        print(oftype)
        if oftype in self._mmap :
            self._mmap[oftype](msg)
        else :
            if oftype == OFP.OFPT_HELLO :
                self.handle_ofpt_hello(msg)

    def dataReceived(self, data):
        self._dispath_openflow_message(data)

    def sendData(self,data):
        self.transport.write(data)

    def connectionMade(self):
        self._send_hello()

    def connectionLost(self, reason=connectionDone):
        pass

    def _send_hello(self):
        msg = OFP.hello(self.versions)
        self.sendData(msg)

    def handle_ofpt_hello(self,msg):
        versions = OFP.parse_hello(msg)
        accept_versions = self.versions
        version = OFP.negotiate_version(versions,accept_versions)
        if version :
            self.ofp = OFP.get_ofp_instance(version)
            self._init_msg_map(self.ofp)
        else :
            self.sendData(OFP.hello_failed())

    def handle_ofpt_packet_in(self,msg):
        pass

    def handle_ofpt_features_reply(self,msg):
        pass




class OpenFlowListener(Factory):
    protocol = OpenFlowChannel
    def __init__(self):
        pass

if __name__ == "__main__" :
    of_port = conf.getint("protocol","openflow")
    reactor.listenTCP(of_port,OpenFlowListener())
    reactor.run()
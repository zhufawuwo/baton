#! python3
# coding:utf-8
from twisted.internet import reactor
from twisted.internet.protocol import Protocol,Factory,connectionDone

from pub import *
from openflow import OpenFlowProtocol as OFP


class OpenFlowChannel(Protocol):
    def __init__(self):
        super().__init__()
        self.versions = set(map(float,str(conf.get("protocol","versions")).split('|')))

    def dataReceived(self, data):
        print(data)
        ver,oftype,len,xid = OFP.parse_ofp_header(data)
        if oftype == OFP.OFPT_HELLO :
            self._handle_hello(data)


    def sendData(self,data):
        self.transport.write(data)

    def connectionMade(self):
        self._send_hello()

    def connectionLost(self, reason=connectionDone):
        pass

    def _send_hello(self):
        msg = OFP.hello(self.versions)
        self.sendData(msg)

    def _handle_hello(self,msg):
        versions = OFP.parse_hello(msg)
        accept_versions = self.versions
        version = OFP.negotiate_version(versions,accept_versions)
        if version :
            pass
        else :
            self.sendData(OFP.hello_failed())





class OpenFlowListener(Factory):
    protocol = OpenFlowChannel
    def __init__(self):
        pass

if __name__ == "__main__" :
    of_port = conf.getint("protocol","openflow")
    reactor.listenTCP(of_port,OpenFlowListener())
    reactor.run()
#! python3
# coding:utf-8
from twisted.internet import reactor
from twisted.internet.protocol import Protocol,Factory,connectionDone

from pub import *
from vpc.nos.driver.ovs.openflow import OpenFlowProtocol as OFP


class MBus():
    def __init__(self):
        self._mmap = {}
        self.ofp = OFP.get_ofp_instance(max(OFP.VERSIONS))

    def route(self,mtype):
        def decorator(f):
            self._mmap[mtype] = f
            return f
        return decorator

    def dispatch(self,chn,msg):
        ver,oftype,len,xid = self.ofp.parse_ofp_header(msg)
        handler = self._mmap.get(oftype,None)
        if handler :
            handler(chn,msg)


mbus = MBus()

class OpenFlowChannel(Protocol):
    def __init__(self):
        super().__init__()
        self.ofp = None

    def dataReceived(self, data):
        mbus.dispatch(self,data)

    def sendData(self,data):
        self.transport.write(data)

    def connectionMade(self):
        self.send_hello()

    def connectionLost(self, reason=connectionDone):
        pass

    def send_hello(self):
        msg = OFP.hello(OFP.VERSIONS)
        self.sendData(msg)

    @mbus.route(mbus.ofp.OFPT_HELLO)
    def handle_hello(self,msg):
        versions = OFP.parse_hello(msg)
        accept_versions = OFP.VERSIONS
        version = OFP.negotiate_version(versions,accept_versions)
        if version :
            self.ofp = OFP.get_ofp_instance(version)
        else :
            self.sendData(OFP.hello_failed())

    @mbus.route(mbus.ofp.OFPT_FEATURES_REPLY)
    def handle_features_reply(self,msg):
        pass

    @mbus.route(mbus.ofp.OFPT_PACKET_IN)
    def handle_packet_in(self,msg):
        print(msg)


class OpenFlowListener(Factory):
    protocol = OpenFlowChannel
    def __init__(self):
        pass

if __name__ == "__main__" :
    of_port = conf.getint("protocol","openflow")
    reactor.listenTCP(of_port,OpenFlowListener())
    reactor.run()